"""Tests for Calendar."""

import pytest
from Paxos.Classes.Appointment import Appointment
from Paxos.Classes.Calendar import Calendar

def test___init__():
    """Test construction of Calendar object."""
    def test_TypeError(*appointments):
        """Test TypeError raising during Calendar object construction."""
        with pytest.raises(TypeError) as excinfo:
            Calendar(*appointments)
    def test_ValueError(*appointments):
        """Test ValueError raising during Calendar object construction."""
        with pytest.raises(ValueError) as excinfo:
            Calendar(*appointments)

    a1 = Appointment("yo","saturday","12:30pm","1:30pm", [1, 2, 3])
    a1_copy = Appointment("yo_copy","saturday","12:30pm","1:30pm", [1, 2, 3])
    a2 = Appointment("yerboi","saturday","1:30am","11:30am", [1, 4, 5])
    a3 = Appointment("we out here","saturday","11:30am","12:30pm", [1])

    test_TypeError(a1, None)
    test_TypeError(None)
    test_TypeError(a1, None, a2)
    test_ValueError(a1, a1_copy)

    #test implicit duplicate removal
    c = Calendar(a1, a1, a2, a2, a3, a3)
    assert len(c) == 3

def test___eq__():
    """Test == operator of Calendar object."""
    def test_TypeError(self, other):
        """Test TypeError raising during == of Calendar objects."""
        with pytest.raises(TypeError) as excinfo:
            self == other

    a1 = Appointment("yo","saturday","12:30pm","1:30pm", [1, 2, 3])
    a2 = Appointment("yerboi","saturday","1:30am","11:30am", [1, 4, 5])
    a3 = Appointment("we out here","saturday","11:30am","12:30pm", [1])

    c1 = Calendar(a1, a2, a3)
    c2 = Calendar(a1, a1, a2, a2, a3, a3)
    c3 = Calendar(a3, a1, a2)
    
    test_TypeError(c1, None)
    test_TypeError(c1, a1)
    assert c1 == c1
    assert c1 == c2
    assert c1 == c3
    assert c1 == c2 == c3

def test___iadd__():
    """Test += operator for Calendar object."""
    def test_TypeError(self, other):
        """Test TypeError raising during += operator of Calendar."""
        with pytest.raises(TypeError) as excinfo:
            self += other
    def test_ValueError(self, other):
        """Test ValueError raising during += operator of Calendar."""
        with pytest.raises(ValueError) as excinfo:
            self += other

    a1 = Appointment("yo","saturday","12:30pm","1:30pm", [1, 2, 3])
    a2 = Appointment("yerboi","Friday","1:30am","11:30am", [1, 4, 5])
    a3 = Appointment("we out here","Tuesday","11:30am","12:30pm", [1])
    a4 = Appointment("bluv","Thursday","11:30am","12:30pm", [2, 6])
    a5 = Appointment("blarg","wedneSdaY","11:30am","12:30pm", [1, 2, 3, 4, 5])
    a1_conf = Appointment("yo_conf","saturday","12:30pm","1:30pm", [1, 2, 3])

    c1 = Calendar(a1, a2)
    c2 = Calendar(a3, a4)
    c1_conf = Calendar(a3, a1_conf)

    test_TypeError(c1, None)
    test_TypeError(c1, "")
    test_ValueError(c1, a1_conf)
    test_ValueError(c1, c1_conf)

    #test duplicates get dropped durring addition
    c1 += a1
    assert len(c1) == 2
    c1 += c1
    assert len(c1) == 2
    c1 += c2
    assert c1 == Calendar(a1, a2, a3, a4)
    assert c1 == Calendar(a4, a3, a2, a1)
    c1 += a5
    assert c1 == Calendar(a4, a3, a5, a2, a1)

def test___ne__():
    """Test == operator of Calendar object."""
    def test_TypeError(self, other):
        """Test TypeError raising during != of Calendar objects."""
        with pytest.raises(TypeError) as excinfo:
            self == other

    a1 = Appointment("yo","saturday","12:30pm","1:30pm", [1, 2, 3])
    a2 = Appointment("yerboi","saturday","1:30am","11:30am", [1, 4, 5])
    a3 = Appointment("we out here","saturday","11:30am","12:30pm", [1])

    c1 = Calendar(a1, a2, a3)
    c2 = Calendar(a1, a1, a2, a2, a3, a3)
    c3 = Calendar(a3, a1, a2)
    c4 = Calendar(a3, a1)
    c5 = Calendar(a1)
    
    test_TypeError(c1, None)
    test_TypeError(c1, a1)
    assert not c1 != c1
    assert not c1 != c2
    assert not c1 != c3
    assert not c1 != c2 != c3
    assert c1 != c4
    assert c1 != c5
    assert c4 != c5
    assert c1 != c4 != c5

def test___len__():
    """Test len(Calendar)."""

    a1 = Appointment("yo","saturday","12:30pm","1:30pm", [1, 2, 3])
    a2 = Appointment("yerboi","saturday","1:30am","11:30am", [1, 4, 5])
    a3 = Appointment("we out here","saturday","11:30am","12:30pm", [1])

    c0 = Calendar()
    c1 = Calendar(a1, a2, a3)
    c2 = Calendar(a1, a1, a2, a2, a3, a3)
    assert len(c0) == 0
    assert len(c1) == 3
    assert len(c2) == 3

def test___getitem__():
    """Test Test indexing for Calendar."""
    def test_TypeError(calendar, key):
        """Test TypeError raising during calendar[key]."""
        with pytest.raises(TypeError) as excinfo:
            calendar[key]
    def test_IndexError(calendar, key):
        """Test IndexError raising during calendar[key]."""
        with pytest.raises(IndexError) as excinfo:
            calendar[key]

    a1 = Appointment("yo","saturday","12:30pm","1:30pm", [1, 2, 3])
    a2 = Appointment("yerboi","saturday","1:30am","11:30am", [1, 4, 5])
    a3 = Appointment("we out here","saturday","11:30am","12:30pm", [1])

    c1 = Calendar(a1, a2, a3)

    test_TypeError(c1, None)
    test_TypeError(c1, "yo")
    test_IndexError(c1, 4)
    test_IndexError(c1, 1000000)

    assert c1[0] == a1
    assert c1[0] is a1
    c1[0]._name = "bbz"
    assert a1._name == "bbz"
    assert c1[1] == a2
    assert c1[1] is a2
    assert c1[2] == a3
    assert c1[2] is a3

def test___setitem__():
    """Test Calendar[key] = value."""
    def test_TypeError(calendar, key, value):
        """Test TypeError raising during calendar[key] = value."""
        with pytest.raises(TypeError) as excinfo:
            calendar[key] = value
    def test_IndexError(calendar, key, value):
        """Test IndexError raising during calendar[key] = value."""
        with pytest.raises(IndexError) as excinfo:
            calendar[key] = value
    def test_ValueError(calendar, key, value):
        """Test ValueError raising during calendar[key] = value."""
        with pytest.raises(ValueError) as excinfo:
            calendar[key] = value

    a1 = Appointment("yo","saturday","12:30pm","1:30pm", [1, 2, 3])
    a1_copy = Appointment("yo_copy","saturday","12:30pm","1:30pm", [1, 2, 3])
    a2 = Appointment("yerboi","saturday","1:30am","11:30am", [1, 4, 5])
    a3 = Appointment("we out here","saturday","11:30am","12:30pm", [1])

    c1 = Calendar(a1, a2)

    #Test non Appointment object value
    test_TypeError(c1, 0, None)
    test_TypeError(c1, 0, c1)
    #Test non int index
    test_TypeError(c1, None, a3)
    test_TypeError(c1, "", a3)
    #test bad index
    test_IndexError(c1, 4, a3)
    test_IndexError(c1, 10000, a3)
    #test conflicted addition
    test_ValueError(c1, 1, a1_copy)
    #test duplicate entry
    test_ValueError(c1, 1, a1)

    c1[1] = a3
    assert c1[1] == a3
    assert c1[1] is a3

def test___iter__():
    """Test iterator for Calendar object."""
    
    a1 = Appointment("yo","saturday","12:30pm","1:30pm", [1, 2, 3])
    a2 = Appointment("yerboi","saturday","1:30am","11:30am", [1, 4, 5])
    a3 = Appointment("we out here","saturday","11:30am","12:30pm", [1])

    c1 = Calendar(a1, a2, a3)

    assert [appt for appt in c1] == c1._appointments
    assert [i for i in iter(c1)] == c1._appointments
    
    for i, appt in enumerate(c1):
        if i == 0: 
            assert appt == a1
            assert appt is a1
        if i == 1: 
            assert appt == a2
            assert appt is a2
        if i == 2: 
            assert appt == a3
            assert appt is a3

def test___contains__():
    """
    Test 'in' and 'not in' operators for Calendar.
    
    Appointment class catches TypeErrors so ignore here.
    """
    
    a1 = Appointment("yo","saturday","12:30pm","1:30pm", [1, 2, 3])
    a2 = Appointment("yerboi","saturday","1:30am","11:30am", [1, 4, 5])
    a3 = Appointment("we out here","saturday","11:30am","12:30pm", [1])

    c1 = Calendar(a1, a2)

    assert a1 in c1
    assert a2 in c1
    assert a3 not in c1

def test___deepcopy__():
    """Implement copy.deepcopy for Calendar object."""
    from copy import deepcopy
    a1 = Appointment("yo","saturday","12:30pm","1:30pm", [1, 2, 3])
    a2 = Appointment("yerboi","Friday","1:30am","11:30am", [1, 4, 5])
    a3 = Appointment("we out here","Tuesday","11:30am","12:30pm", [1])
    a4 = Appointment("bluv","Thursday","11:30am","12:30pm", [2, 6])

    c = Calendar(a1, a2, a3, a4)
    c_copy = deepcopy(c)
    assert c == c_copy
    assert c is not c_copy
    appts = c._appointments
    appts_copy = c_copy._appointments
    for i in range(len(appts)):
        assert appts[i] == appts_copy[i]
        assert appts[i] is not appts_copy[i]

def test__is_appointment_conflicting():
    """Test Calendar's _is_appointment_conflicting() function."""
    def test_TypeError(calendar, appointment):
        """Test TypeError raising during _is_appointment_conflicting()."""
        with pytest.raises(TypeError) as excinfo:
            calendar._is_appointment_conflicting(appointment)

    a1 = Appointment("yo","saturday","12:30pm","1:30pm", [1, 2, 3])
    a1_copy = Appointment("yo_copy","saturday","12:30pm","1:30pm", [1, 2, 3])
    a2 = Appointment("yerboi","saturday","1:30am","11:30am", [1, 4, 5])
    a3 = Appointment("we out here","saturday","11:30am","12:30pm", [1])

    c1 = Calendar(a1, a2)

    test_TypeError(c1, None)
    test_TypeError(c1, "Appointment")

    assert not c1._is_appointment_conflicting(a1)
    assert c1._is_appointment_conflicting(a1_copy)
    assert not c1._is_appointment_conflicting(a3)

def test__is_calendar_conflicting():
    """Test Calendar's _is_calendar_conflicting() function."""
    def test_TypeError(calendar1, calendar2):
        """Test TypeError raising during calendar[key] = value."""
        with pytest.raises(TypeError) as excinfo:
            calendar1._is_calendar_conflicting(calendar2)

    a1 = Appointment("yo","saturday","12:30pm","1:30pm", [1, 2, 3])
    a2 = Appointment("yerboi","Friday","1:30am","11:30am", [1, 4, 5])
    a3 = Appointment("we out here","Tuesday","11:30am","12:30pm", [1])
    a4 = Appointment("bluv","Thursday","11:30am","12:30pm", [2, 6])
    a5 = Appointment("yo_conflict","saturday","12:30pm","1:30pm", [1, 2, 6])

    c1 = Calendar(a1, a2)
    c2 = Calendar(a3, a4)
    c3 = Calendar(a1, a3)
    c4 = Calendar(a4, a5)

    test_TypeError(c1, None)
    test_TypeError(c1, "Calendar")

    #test identity not conflicting
    assert not c1._is_calendar_conflicting(c1)
    #regular disjoint test
    assert not c1._is_calendar_conflicting(c2)
    assert not c2._is_calendar_conflicting(c1)
    #test shared (but equal) appointment not conflicting
    assert not c1._is_calendar_conflicting(c3)
    assert not c3._is_calendar_conflicting(c1)
    #test disjoint but conflicting calendars
    assert c1._is_calendar_conflicting(c4)
    assert c4._is_calendar_conflicting(c1)
