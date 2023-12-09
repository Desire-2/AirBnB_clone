#!/usr/bin/python3
"""Defines unittests for models/user.py.
Unittest classes:
    TestUser_instantiation
    TestUser_save
    TestUser_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.user import User


class TestUser_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the User class."""

    def testNoArgsInstantiates(self):
        self.assertEqual(User, type(User()))

    def testNewInstanceStoredInObjects(self):
        self.assertIn(User(), models.storage.all().values())

    def test_id_isPublicStr(self):
        self.assertEqual(str, type(User().id))

    def testCreated_at_isPublicDatetime(self):
        self.assertEqual(datetime, type(User().created_at))

    def testUpdated_at_isPublicDatetime(self):
        self.assertEqual(datetime, type(User().updated_at))

    def testEmail_isPublicStr(self):
        self.assertEqual(str, type(User.email))

    def testPassword_isPublicStr(self):
        self.assertEqual(str, type(User.password))

    def testFirstName_isPublicStr(self):
        self.assertEqual(str, type(User.first_name))

    def testLastName_isPublicStr(self):
        self.assertEqual(str, type(User.last_name))

    def testTwoUsersUniqueIds(self):
        us1 = User()
        us2 = User()
        self.assertNotEqual(us1.id, us2.id)

    def testTwoUsersDifferentCreated_at(self):
        us1 = User()
        sleep(0.05)
        us2 = User()
        self.assertLess(us1.created_at, us2.created_at)

    def testTwoUsersDifferentUpdated_at(self):
        us1 = User()
        sleep(0.05)
        us2 = User()
        self.assertLess(us1.updated_at, us2.updated_at)

    def testStrRepresentation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        us = User()
        us.id = "123456"
        us.created_at = us.updated_at = dt
        usstr = us.__str__()
        self.assertIn("[User] (123456)", usstr)
        self.assertIn("'id': '123456'", usstr)
        self.assertIn("'created_at': " + dt_repr, usstr)
        self.assertIn("'updated_at': " + dt_repr, usstr)

    def testArgsUnused(self):
        us = User(None)
        self.assertNotIn(None, us.__dict__.values())

    def testInstantiationWithKwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        us = User(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(us.id, "345")
        self.assertEqual(us.created_at, dt)
        self.assertEqual(us.updated_at, dt)

    def testInstantiationWithNoneKwargs(self):
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)


class TestUser_save(unittest.TestCase):
    """Unittests for testing save method of the  class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def testOneSave(self):
        us = User()
        sleep(0.05)
        first_updated_at = us.updated_at
        us.save()
        self.assertLess(first_updated_at, us.updated_at)

    def testTwoSaves(self):
        us = User()
        sleep(0.05)
        first_updated_at = us.updated_at
        us.save()
        second_updated_at = us.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        us.save()
        self.assertLess(second_updated_at, us.updated_at)

    def testSaveWithArg(self):
        us = User()
        with self.assertRaises(TypeError):
            us.save(None)

    def testSaveUpdatesFile(self):
        us = User()
        us.save()
        usid = "User." + us.id
        with open("file.json", "r") as f:
            self.assertIn(usid, f.read())


class TestUser_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the User class."""

    def test_to_dictType(self):
        self.assertTrue(dict, type(User().to_dict()))

    def test_to_dictContainsCorrectKeys(self):
        us = User()
        self.assertIn("id", us.to_dict())
        self.assertIn("created_at", us.to_dict())
        self.assertIn("updated_at", us.to_dict())
        self.assertIn("__class__", us.to_dict())

    def test_to_dictContainsAddedAttributes(self):
        us = User()
        us.middle_name = "Alx"
        us.my_number = 98
        self.assertEqual("Alx", us.middle_name)
        self.assertIn("my_number", us.to_dict())

    def test_to_dictDatetimeAttributesAreStrs(self):
        us = User()
        us_dict = us.to_dict()
        self.assertEqual(str, type(us_dict["id"]))
        self.assertEqual(str, type(us_dict["created_at"]))
        self.assertEqual(str, type(us_dict["updated_at"]))

    def test_to_dictOutput(self):
        dt = datetime.today()
        us = User()
        us.id = "123456"
        us.created_at = us.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'User',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(us.to_dict(), tdict)

    def testContrast_to_dictDunderDict(self):
        us = User()
        self.assertNotEqual(us.to_dict(), us.__dict__)

    def test_to_dictWithArg(self):
        us = User()
        with self.assertRaises(TypeError):
            us.to_dict(None)


if __name__ == "__main__":
    unittest.main()
