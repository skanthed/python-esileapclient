from tempest.lib.exceptions import CommandFailed
from tempest.lib import decorators
from tempest.lib.common.utils import data_utils

import esileapclient.tests.functional.utils.esi_interfaces as esi
from esileapclient.tests.functional.base import ESIBaseTestClass
from esileapclient.tests.functional.utils.dummy_node import DummyNode


class BasicTests(ESIBaseTestClass):
    @classmethod
    def setUpClass(cls):
        super(BasicTests, cls).setUpClass()
        cls._init_dummy_project(cls, 'parent', ['owner'])
        cls._init_dummy_project(cls, 'child', ['lessee'], parent='parent')

    def setUp(self):
        super(BasicTests, self).setUp()
        self.clients = BasicTests.clients
        self.users = BasicTests.users
        self.projects = BasicTests.projects
        self.dummy_node = DummyNode(BasicTests.config['dummy_node_dir'],
                                    self.projects['parent']['id'])

    def test_offer_owner(self):
        """ Tests basic functionality of "esi offer create/list/show/delete"
                when executed by a node-owning project.
            Test steps:
            1) Create an offer for an owned node.
            2) Check that offer details were returned.
            3) Check that the output of 'offer list' contains the new offer.
            4) Check that the output of 'offer show' contains the details of
                the new offer.
            5) (cleanup) Delete the offer created in step 1. """
        offer = esi.offer_create(self.clients['parent-owner'],
                                 self.dummy_node.uuid,
                                 resource_type='dummy_node')
        self.assertNotEqual(offer, {})
        self.addCleanup(esi.offer_delete,
                        self.clients['parent-owner'],
                        offer['uuid'])

        details = esi.offer_show(self.clients['parent-owner'], offer['uuid'])
        for field in offer.keys():
            self.assertEqual(offer[field], details[field])

        listings = esi.offer_list(self.clients['parent-owner'])
        self.assertNotEqual(listings, [])
        self.assertIn(offer['uuid'], [x['UUID'] for x in listings])

    def test_lease_owner(self):
        """ Tests basic functionality of "esi lease create/list/show/delete"
                when called by an owner.
            Test steps:
            1) Create a lease for an owned node for the lessee.
            2) Check that lease details were returned.
            3) Check that the output of 'lease list' contains the new lease.
            4) Check that the output of 'lease show' contains the details of
                the new lease.
            5) (cleanup) Delete the lease created in step 1. """
        lease = esi.lease_create(self.clients['parent-owner'],
                                 self.dummy_node.uuid,
                                 self.projects['child']['name'],
                                 resource_type='dummy_node',
                                 start_time='9999-01-01')
        self.assertNotEqual(lease, {})
        self.addCleanup(esi.lease_delete,
                        self.clients['parent-owner'],
                        lease['uuid'])

        details = esi.lease_show(self.clients['parent-owner'], lease['uuid'])
        for field in lease.keys():
            self.assertEqual(lease[field], details[field])

        listings = esi.lease_list(self.clients['parent-owner'])
        self.assertNotEqual(listings, [])
        self.assertIn(lease['uuid'], [x['UUID'] for x in listings])

    def test_offer_lessee(self):
        """ Tests basic functionality of "esi offer claim/show/list" when
                called by a lessee.
            Test steps:
            1) (owner) Create an offer for an owned node for the lessee.
            2) (owner) Check that offer details were returned.
            3) (lessee) Check that the output of 'offer list' contains the
                new offer.
            4) (lessee) Check that the output of 'offer show' contains the
                details of the new offer.
            5) (lessee) Claim the offer created in step 1.
            6) (lessee) Check that lease details were returned.
            7) (lessee) (cleanup) Delete the lease created in step 5.
            8) (owner) (cleanup) Delete the offer created in step 1. """
        offer = esi.offer_create(self.clients['parent-owner'],
                                 self.dummy_node.uuid,
                                 lessee=self.projects['child']['name'],
                                 resource_type='dummy_node')
        self.assertNotEqual(offer, {})
        self.addCleanup(esi.offer_delete,
                        self.clients['parent-owner'],
                        offer['uuid'])

        details = esi.offer_show(self.clients['child-lessee'], offer['uuid'])
        for field in offer.keys():
            self.assertEquals(offer[field], details[field])

        listings = esi.offer_list(self.clients['child-lessee'])
        self.assertNotEqual(listings, [])
        self.assertIn(offer['uuid'], [x['UUID'] for x in listings])

        lease = esi.offer_claim(self.clients['child-lessee'], offer['uuid'])
        self.assertNotEqual(lease, {})
        self.addCleanup(esi.lease_delete,
                        self.clients['child-lessee'],
                        lease['uuid'])

    def test_lease_lessee(self):
        """ Tests basic functionality of "esi lease show/list/delete" when
                called by a lessee.
            Test steps:
            1) (owner) Create a lease for an owned node for the lessee.
            2) (owner) Check that lease details were returned.
            3) (lessee) Check that the output of 'lease list' contains the
                new lease.
            4) (lessee) Check that the output of 'lease show' contains the
                details of the new lease.
            5) (lessee) (cleanup) Delete the lease created in step 1. """
        lease = esi.lease_create(self.clients['parent-owner'],
                                 self.dummy_node.uuid,
                                 self.projects['child']['name'],
                                 resource_type='dummy_node',
                                 start_time='9999-01-01')
        self.assertNotEqual(lease, {})
        self.addCleanup(esi.lease_delete,
                        self.clients['child-lessee'],
                        lease['uuid'])

        details = esi.lease_show(self.clients['child-lessee'], lease['uuid'])
        for field in lease.keys():
            self.assertEqual(lease[field], details[field])

        listings = esi.lease_list(self.clients['child-lessee'])
        self.assertNotEqual(listings, [])
        self.assertIn(lease['uuid'], [x['UUID'] for x in listings])

    @decorators.attr(type=['negative'])
    def test_show_invalid_id(self):
        """ Tests that "esi [offer/lease] show" properly handles being
                passed a offer/lease uuid that does not exist.
            Test steps:
            1) Attempt to show details of an offer that does not exist.
            2) Check that the command failed. (returned non-zero exit code)
            3) Check that the proper error message was sent to stderr.
            4) Attempt to show details of a lease that does not exist.
            5) Check that the command failed. (returned non-zero exit code)
            6) Check that the proper error message was sent to stderr. """
        fake_name = data_utils.rand_name('does-not-exist', prefix='')
        e = self.assertRaises(CommandFailed,
                              esi.offer_show,
                              self.clients['parent-owner'],
                              fake_name)
        self.assertIn('Offer with name or uuid %s not found.' % fake_name,
                      e.stderr.decode())

        e = self.assertRaises(CommandFailed,
                              esi.lease_show,
                              self.clients['parent-owner'],
                              fake_name)
        self.assertIn('Lease with name or uuid %s not found.' % fake_name,
                      e.stderr.decode())

    @decorators.attr(type=['negative'])
    def test_delete_invalid_id(self):
        """ Tests that "esi [offer/lease] delete" properly handles being
                passed a offer/lease uuid that does not exist.
            Test steps:
            1) Attempt to delete an offer that does not exist.
            2) Check that the command failed. (returned non-zero exit code)
            3) Check that the proper error message was sent to stderr.
            4) Attempt to delete a lease that does not exist.
            5) Check that the command failed. (returned non-zero exit code)
            6) Check that the proper error message was sent to stderr. """
        fake_name = data_utils.rand_name('does-not-exist', prefix='')
        e = self.assertRaises(CommandFailed,
                              esi.offer_delete,
                              self.clients['parent-owner'],
                              fake_name)
        self.assertIn('Offer with name or uuid %s not found.' % fake_name,
                      e.stderr.decode())

        e = self.assertRaises(CommandFailed,
                              esi.lease_delete,
                              self.clients['parent-owner'],
                              fake_name)
        self.assertIn('Lease with name or uuid %s not found.' % fake_name,
                      e.stderr.decode())

    @decorators.attr(type=['negative'])
    def test_offer_claim_invalid_id(self):
        """ Tests that "esi offer claim" properly handles being passed an
                offer uuid that does not exist.
            Test steps:
            1) Attempt to claim an offer that does not exist.
            2) Check that the command failed. (returned non-zero exit code)
            3) Check that the proper error message was sent to stderr. """
        fake_name = data_utils.rand_name('does-not-exist', prefix='')
        e = self.assertRaises(CommandFailed,
                              esi.offer_claim,
                              self.clients['child-lessee'],
                              fake_name)
        self.assertIn('Offer with name or uuid %s not found.' % fake_name,
                      e.stderr.decode())

    @decorators.attr(type=['negative'])
    def test_offer_create_invalid_node(self):
        """ Tests that "esi [offer/lease] create" properly handles being
                passed a resource node uuid that does not exist.
            Test steps:
            1) Attempt to create an offer for a node that does not exist.
            2) Check that the command failed. (returned non-zero exit code)
            3) Attempt to create a lease for a node that does not exist.
            4) Check that the command failed. (returned non-zero exit code) """
        fake_name = data_utils.rand_name('does-not-exist', prefix='')
        e = self.assertRaises(CommandFailed,
                              esi.offer_create,
                              self.clients['parent-owner'],
                              fake_name,
                              resource_type='dummy_node')
        self.assertIn('No such file or directory', e.stderr.decode())

        e = self.assertRaises(CommandFailed,
                              esi.lease_create,
                              self.clients['parent-owner'],
                              fake_name,
                              self.projects['child']['name'],
                              resource_type='dummy_node')
        self.assertIn('No such file or directory', e.stderr.decode())
