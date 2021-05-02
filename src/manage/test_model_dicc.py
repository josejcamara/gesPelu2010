import unittest
import sys, os
import model_dicc

TEST_DB_NAME = 'test_dicc.db'

class TestModelDicc(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('\nPreparing testDB: %s' % TEST_DB_NAME)
        cls._engine = model_dicc.Dicc('.',TEST_DB_NAME)

    @classmethod
    def tearDownClass(cls):
        print('\nRemoving testDB: %s' % TEST_DB_NAME)
        os.remove(TEST_DB_NAME)

    def test_createDicc_whenDiccDoesNotExists_shouldSuccess(self):
        """ It covers 'createDicc' and 'getDiccList' """
        NEW_DICC_NAME = 'newDicc'
        statusCreated = self._engine.createDicc(NEW_DICC_NAME)
        listOfDicc = self._engine.getDiccList()
        #
        self.assertEqual(statusCreated, 0, "Creation status for %s should be 0 but it is %d." % (NEW_DICC_NAME,statusCreated))
        self.assertTrue(NEW_DICC_NAME in listOfDicc,"List should contains new created Dicc")

    def test_createDicc_whenDiccAlreadyExists_shouldFail(self):
        """ It covers 'createDicc' and 'getDiccList' """
        NEW_DICC_NAME = 'newDicc2'
        statusCreated = self._engine.createDicc(NEW_DICC_NAME)
        listOfDicc = self._engine.getDiccList()
        statusCreatedSecond = self._engine.createDicc(NEW_DICC_NAME)
        #
        self.assertEqual(statusCreated, 0, "Creation status for %s should be 0 but it is %d." % (NEW_DICC_NAME,statusCreated))
        self.assertTrue(NEW_DICC_NAME in listOfDicc,"List should contains new created Dicc")
        self.assertNotEqual(statusCreatedSecond, 0, "Creation status should be 0 but it is %d" % statusCreatedSecond)

    def test_deleteDicc_whenDiccAlreadyExists_shouldSuccess(self):
        """ It covers 'createDicc', 'getDiccList' and 'deleteDicc' """
        NEW_DICC_NAME = 'newDicc3'
        statusCreated = self._engine.createDicc(NEW_DICC_NAME)
        listOfDicc = self._engine.getDiccList()
        #
        self.assertEqual(statusCreated, 0, "Creation status for %s should be 0 but it is %d." % (NEW_DICC_NAME,statusCreated))
        self.assertTrue(NEW_DICC_NAME in listOfDicc,"List should contains new created Dicc")
        #
        statusDeleted = self._engine.deleteDicc(NEW_DICC_NAME)
        listOfDicc = self._engine.getDiccList()
        #
        self.assertEqual(statusDeleted, 0, "Deletion status for %s should be 0 but it is %d." % (NEW_DICC_NAME,statusDeleted))
        self.assertFalse(NEW_DICC_NAME in listOfDicc,"List should NOT contains new created Dicc")
        #

    def test_deleteDicc_whenDiccDoesNotExists_shouldFail(self):
        """ It covers 'getDiccList' and 'deleteDicc' """
        NEW_DICC_NAME = 'newDicc4'
        listOfDicc = self._engine.getDiccList()
        #
        self.assertFalse(NEW_DICC_NAME in listOfDicc,"List should NOT contain %s Dicc" % NEW_DICC_NAME)
        #
        statusDeleted = self._engine.deleteDicc(NEW_DICC_NAME)
        #
        self.assertNotEqual(statusDeleted, 0, "Deletion status for %s should NOT be 0" % NEW_DICC_NAME)

    def test_getDiccHeader_whenDiccExists(self):
        """ It covers 'createDicc', 'updateDicc', 'getDiccHeader' """
        NEW_DICC_NAME = 'newDicc5'
        NEW_DICC_HEADER = [NEW_DICC_NAME,'tabla prueba',10,'rel','index','accion']
        NEW_DICC_ROWS = []

        statusCreated = self._engine.createDicc(NEW_DICC_NAME)
        listOfDicc = self._engine.getDiccList()
        #
        self.assertEqual(statusCreated, 0, "Creation status for %s should be 0 but it is %d." % (NEW_DICC_NAME,statusCreated))
        self.assertTrue(NEW_DICC_NAME in listOfDicc,"List should contains new created Dicc")
        #
        self._engine.updateDicc(NEW_DICC_NAME, NEW_DICC_HEADER, NEW_DICC_ROWS)
        #
        headerDicc = self._engine.getDiccHeader(NEW_DICC_NAME)
        print(headerDicc)

    def test_getDiccHeader_whenDiccDoesNotExists(self):
        """ It covers getDiccHeader """
        NEW_DICC_NAME = 'newDicc6'
        headerDicc = self._engine.getDiccHeader(NEW_DICC_NAME)
        #
        self.assertEqual(headerDicc, [], "getDiccHeader should return empty list, but returns "+str(headerDicc))

    def test_getDiccRows_whenDiccExists(self):
        pass

    def test_getDiccRows_whenDiccDoesNotExists(self):
        pass

    def test_updateDicc_whenDiccExists(self):
        pass

    def test_updateDicc_whenDiccDoesNotExists(self):
        pass

def prepare_test_data():
    db = model_dicc.Dicc('.',TEST_DB_NAME)
    return db

def delete_test_data():
    pass

if __name__ == '__main__':
    prepare_test_data()
    unittest.main()
    delete_test_data()

