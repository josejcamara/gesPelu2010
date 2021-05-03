import unittest
import sys, os

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
        expectedList = [NEW_DICC_NAME,'']
        self.assertEqual(statusCreated, 0, "Creation status for %s should be 0 but it is %d." % (NEW_DICC_NAME,statusCreated))
        self.assertTrue(expectedList in listOfDicc,"getDiccList should contain new created Dicc %s, but contains instead %s." % (str(expectedList), str(listOfDicc)))

    def test_createDicc_whenDiccAlreadyExists_shouldFail(self):
        """ It covers 'createDicc' and 'getDiccList' """
        NEW_DICC_NAME = 'newDicc2'
        statusCreated = self._engine.createDicc(NEW_DICC_NAME)
        listOfDicc = self._engine.getDiccList()
        statusCreatedSecond = self._engine.createDicc(NEW_DICC_NAME)
        #
        expectedList = [NEW_DICC_NAME,'']
        self.assertEqual(statusCreated, 0, "Creation status for %s should be 0 but it is %d." % (NEW_DICC_NAME,statusCreated))
        self.assertTrue(expectedList in listOfDicc,"getDiccList should contain new created Dicc '%s' but contains instead %s." % (str(expectedList),str(listOfDicc)))
        self.assertNotEqual(statusCreatedSecond, 0, "Creation status should be 0 but it is %d" % statusCreatedSecond)

    def test_deleteDicc_whenDiccAlreadyExists_shouldSuccess(self):
        """ It covers 'createDicc', 'getDiccList' and 'deleteDicc' """
        NEW_DICC_NAME = 'newDicc3'
        statusCreated = self._engine.createDicc(NEW_DICC_NAME)
        listOfDicc = self._engine.getDiccList()
        #
        expectedList = [NEW_DICC_NAME,'']
        self.assertEqual(statusCreated, 0, "Creation status for %s should be 0 but it is %d." % (NEW_DICC_NAME,statusCreated))
        self.assertTrue(expectedList in listOfDicc,"getDiccList should contain new created Dicc '%s' but contains instead %s." % (str(expectedList),str(listOfDicc)))
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

    def test_getDicc(self):
        """ It covers 'createDicc', 'updateDicc', 'getDiccHeader' and 'getDiccRows' """
        NEW_DICC_NAME = 'newDicc5'
        NEW_DICC_HEADER = ['tabla prueba',10,'rel','index','accion']
        NEW_DICC_ROWS = []

        statusCreated = self._engine.createDicc(NEW_DICC_NAME)
        listOfDicc = self._engine.getDiccList()
        #
        expectedList = [NEW_DICC_NAME,'']
        self.assertEqual(statusCreated, 0, "Creation status for %s should be 0 but it is %d." % (NEW_DICC_NAME,statusCreated))
        self.assertTrue(expectedList in listOfDicc,"getDiccList should contain new created Dicc '%s' but contains instead %s." % (str(expectedList),str(listOfDicc)))
        #
        self._engine.updateDicc(NEW_DICC_NAME, NEW_DICC_HEADER, NEW_DICC_ROWS)
        #
        data = self._engine.getDicc(NEW_DICC_NAME)
        self.assertEquals(data[0],'tabla prueba')
        self.assertEquals(data[1],10)
        self.assertEquals(data[2],'rel')
        self.assertEquals(data[3],'index')
        self.assertEquals(data[4],'accion')
        self.assertEquals(data[5],NEW_DICC_ROWS)


    def test_getDiccHeader_whenDiccExists(self):
        """ It covers 'createDicc', 'updateDicc', 'getDiccHeader' """
        NEW_DICC_NAME = 'newDicc6'
        NEW_DICC_HEADER = ['tabla prueba',10,'rel','index','accion']
        NEW_DICC_ROWS = []

        statusCreated = self._engine.createDicc(NEW_DICC_NAME)
        listOfDicc = self._engine.getDiccList()
        #
        expectedList = [NEW_DICC_NAME,'']
        self.assertEqual(statusCreated, 0, "Creation status for %s should be 0 but it is %d." % (NEW_DICC_NAME,statusCreated))
        self.assertTrue(expectedList in listOfDicc,"getDiccList should contain new created Dicc '%s' but contains instead %s." % (str(expectedList),str(listOfDicc)))
        #
        self._engine.updateDicc(NEW_DICC_NAME, NEW_DICC_HEADER, NEW_DICC_ROWS)
        #
        headerDicc = self._engine.getDiccHeader(NEW_DICC_NAME)
        #
        self.assertEquals(headerDicc[0],'tabla prueba')
        self.assertEquals(headerDicc[1],10)
        self.assertEquals(headerDicc[2],'rel')
        self.assertEquals(headerDicc[3],'index')
        self.assertEquals(headerDicc[4],'accion')

    def test_getDiccHeader_whenDiccDoesNotExists(self):
        """ It covers getDiccHeader """
        NEW_DICC_NAME = 'newDicc7'
        headerDicc = self._engine.getDiccHeader(NEW_DICC_NAME)
        #
        self.assertEqual(headerDicc, [], "getDiccHeader should return empty list, but returns "+str(headerDicc))

    def test_getDiccRows_whenDiccExists(self):
        """ It covers 'createDicc', 'updateDicc', 'getDiccHeader' """
        NEW_DICC_NAME = 'newDicc8'
        NEW_DICC_HEADER = [NEW_DICC_NAME,'tabla prueba',10,'rel','index','accion']
        NEW_DICC_ROWS = [ ['campo8','desc','fmt','rel','fcal'] ]

        statusCreated = self._engine.createDicc(NEW_DICC_NAME)
        listOfDicc = self._engine.getDiccList()
        #
        expectedList = [NEW_DICC_NAME,'']
        self.assertEqual(statusCreated, 0, "Creation status for %s should be 0 but it is %d." % (NEW_DICC_NAME,statusCreated))
        self.assertTrue(expectedList in listOfDicc,"getDiccList should contain new created Dicc '%s' but contains instead %s." % (str(expectedList),str(listOfDicc)))
        #
        self._engine.updateDicc(NEW_DICC_NAME, NEW_DICC_HEADER, NEW_DICC_ROWS)
        #
        rowsDicc = self._engine.getDiccRows(NEW_DICC_NAME)
        #
        self.assertEquals(rowsDicc, NEW_DICC_ROWS)


    def test_getDiccRows_whenDiccDoesNotExists(self):
        """ It covers getDiccHeader """
        NEW_DICC_NAME = 'newDicc9'
        rowsDicc = self._engine.getDiccRows(NEW_DICC_NAME)
        #
        self.assertEqual(rowsDicc, [], "getDiccRows should return empty list, but returns "+str(rowsDicc))

    def test_updateDicc_whenDiccExists_shouldUpdate(self):
        """ It covers 'updateDicc' and 'getDicc' """
        NEW_DICC_NAME = 'newDicc10'
        NEW_DICC_HEADER = ['tabla prueba',10,'rel','index','accion']
        NEW_DICC_ROWS = [ ['campo10','desc','fmt','rel','fcal'] ]
        #
        statusCreated = self._engine.createDicc(NEW_DICC_NAME)
        listOfDicc = self._engine.getDiccList()
        expectedList = [NEW_DICC_NAME,'']
        self.assertEqual(statusCreated, 0, "Creation status for %s should be 0 but it is %d." % (NEW_DICC_NAME,statusCreated))
        self.assertTrue(expectedList in listOfDicc,"getDiccList should contain new created Dicc '%s' but contains instead %s." % (str(expectedList),str(listOfDicc)))
        #
        statusUpdate = self._engine.updateDicc(NEW_DICC_NAME, NEW_DICC_HEADER, NEW_DICC_ROWS)
        data = self._engine.getDicc(NEW_DICC_NAME)
        self.assertEquals(statusUpdate,0)
        self.assertEquals(data[0],'tabla prueba')
        self.assertEquals(data[1],10)
        self.assertEquals(data[2],'rel')
        self.assertEquals(data[3],'index')
        self.assertEquals(data[4],'accion')
        self.assertEquals(data[5],NEW_DICC_ROWS)

    def test_updateDicc_whenDiccDoesNotExists_shouldCreate(self):
        """ It covers 'updateDicc' and 'getDicc' """
        NEW_DICC_NAME = 'newDicc11'
        NEW_DICC_HEADER = ['tabla prueba',10,'rel','index','accion']
        NEW_DICC_ROWS = [ ['campo11','desc','fmt','rel','fcal'] ]

        statusUpdate = self._engine.updateDicc(NEW_DICC_NAME, NEW_DICC_HEADER, NEW_DICC_ROWS)
        #
        data = self._engine.getDicc(NEW_DICC_NAME)
        self.assertEquals(statusUpdate,0)
        self.assertEquals(data[0],'tabla prueba')
        self.assertEquals(data[1],10)
        self.assertEquals(data[2],'rel')
        self.assertEquals(data[3],'index')
        self.assertEquals(data[4],'accion')
        self.assertEquals(data[5],NEW_DICC_ROWS)


def confirm(message):
    """
    Ask user to enter Y or N (case-insensitive).
    :return: True if the answer is Y.
    :rtype: bool
    """
    answer = ""
    while answer not in ["y", "n"]:
        answer = raw_input(message + " [Y/N]? ").lower()
    return answer == "y"

if __name__ == '__main__':

    testBSD = confirm('Quieres ejecutar antiguos?')
    if (testBSD):
        import model_dicc_berkeley as model_dicc
        print('=== Testing DSDDB ===')
    else:
        import model_dicc
        print('=== Testing SQLITE ===')

    unittest.main()

