"""Test Appointment object."""

import pytest
from Paxos.Classes.Appointment import Appointment

def test___init__():
    """Test ."""
    def test_TypeError(n, d, s, e, p):
        """Test TypeError raising during Appointment object construction."""
        with pytest.raises(TypeError) as excinfo:
            Appointment(n, d, s, e, p)
    def test_ValueError(n, d, s, e, p):
        """Test ValueError raising during Appointment object construction."""
        with pytest.raises(ValueError) as excinfo:
            Appointment(n, d, s, e, p)

    name, bad_name = "name", None
    day, bad_day_t, bad_day_v = "Saturday", None, "Flendersday"
    start, end = "12:00pm", "1:00pm"
    bad_start_v, bad_end_v = "1:00pm", "12:00pm"
    participants, bad_participants_t1, bad_participants_t2, bad_participants_v = [1, 2, 3], None, ['a', 1], []

    test_TypeError(bad_name, day, start, end, participants)
    test_TypeError(name, bad_day_t, start, end, participants)
    test_ValueError(name, bad_day_v, start, end, participants)
    test_ValueError(name, day, bad_start_v, bad_end_v, participants)
    test_TypeError(name, day, start, end, bad_participants_t1)
    test_TypeError(name, day, start, end, bad_participants_t2)
    test_ValueError(name, day, start, end, bad_participants_v)

def test___eq__():
    """Test == operator for Appointment objects."""
    def test_TypeError(self, other):
        """Test TypeError raising during == of Appointment objects."""
        with pytest.raises(TypeError) as excinfo:
            self == other

    name, day, start, end, participants = "a", "Friday", "1:00pm", "2:00pm", [1]
    A1 = Appointment(name, day, start, end, participants)
    test_TypeError(A1, None)
    assert A1 == A1
    A2 = Appointment('b', day, start, end, participants)
    assert not A1 == A2
    A3 = Appointment(name, "Saturday", start, end, participants)
    assert not A1 == A3
    A4 = Appointment(name, day, "11:00am", end, participants)
    assert not A1 == A4
    A5 = Appointment(name, day, start, "3:00pm", participants)
    assert not A1 == A5
    A6 = Appointment(name, day, start, end, [2])
    assert not A1 == A6
    A7 = Appointment(name, day, start, end, [1,2])
    assert not A1 == A7

def test___ne__():
    """Test == operator for Appointment objects."""
    def test_TypeError(self, other):
        """Test TypeError raising during != of Appointment objects."""
        with pytest.raises(TypeError) as excinfo:
            self == other

    name, day, start, end, participants = "a", "Friday", "1:00pm", "2:00pm", [1]
    A1 = Appointment(name, day, start, end, participants)
    test_TypeError(A1, None)
    assert not A1 != A1
    A2 = Appointment('b', day, start, end, participants)
    assert A1 != A2
    A3 = Appointment(name, "Saturday", start, end, participants)
    assert A1 != A3
    A4 = Appointment(name, day, "11:00am", end, participants)
    assert A1 != A4
    A5 = Appointment(name, day, start, "3:00pm", participants)
    assert A1 != A5
    A6 = Appointment(name, day, start, end, [2])
    assert A1 != A6
    A7 = Appointment(name, day, start, end, [1,2])
    assert A1 != A7

def test__key():
    """Test key function for Appointment."""
    from datetime import time
    name, day, start, end, participants = "a", "Friday", "1:00pm", "2:00pm", [1]
    A1 = Appointment(name, day, start, end, participants)

    assert A1._key() == (name, day, time(13, 0), time(14, 0), (1,))

def test___hash__():
    """Test hashing for Appointment object."""
    name, day, start, end, participants = "a", "Friday", "1:00pm", "2:00pm", [1]
    A1 = Appointment(name, day, start, end, participants)
    A2 = Appointment(name, day, start, end, participants)
    assert hash(A1) == hash(A2)

def test__parse_time():
    """Test static function _parse_time()."""
    from datetime import time

    def test_TypeError(time):
        """Test TypeError raising during Appointment._parse_time()."""
        with pytest.raises(TypeError) as excinfo:
            Appointment._parse_time(time)
    def test_ValueError(time):
        """Test ValueError raising during Appointment._parse_time()."""
        with pytest.raises(ValueError) as excinfo:
            Appointment._parse_time(time)    

    test_TypeError(None)
    test_TypeError(object)
    test_ValueError("string")
    test_ValueError("1::00pm")
    test_ValueError("1:0pm")
    test_ValueError("110:0pm")
    test_ValueError("11:00")
    test_ValueError("13:00am")
    test_ValueError("-1:00am")
    test_ValueError("15:00pm")
    test_ValueError("1:15am")
    test_ValueError("1:07am")
    test_ValueError("1:00gm")
    test_ValueError("1:00m")

    assert Appointment._parse_time("12:00pm") == time(12, 0)
    assert Appointment._parse_time("0:00am") == time(0, 0)
    assert Appointment._parse_time("1:30am") == time(1, 30)
    assert Appointment._parse_time("1:30pm") == time(13, 30)
    assert Appointment._parse_time("11:30pm") == time(23, 30)

def test__is_conflicting():
    """Test Appointment._is_conflicting() static function."""
    def test_TypeError(appt1, appt2):
        """Test TypeError raising during Appointment._is_conflicting()."""
        with pytest.raises(TypeError) as excinfo:
            Appointment._is_conflicting(appt1, appt2)

    name, day, start, end, participants = "a", "Friday", "1:00pm", "2:00pm", [1]
    A1 = Appointment(name, day, start, end, participants)
    A2 = Appointment('b', day, start, end, participants)
    A3 = Appointment(name, "Saturday", start, end, participants)
    A4 = Appointment(name, day, "11:00am", end, participants)
    A5 = Appointment(name, day, start, "3:00pm", participants)
    A6 = Appointment(name, day, start, end, [2])
    A7 = Appointment(name, day, start, end, [1,2])
    A8 = Appointment(name, day, "11:00am", "3:00pm", participants)
    
    test_TypeError(A1, None)
    test_TypeError(None, A1)
    #appointment does not conflict with itself
    assert not Appointment._is_conflicting(A1, A1)
    assert Appointment._is_conflicting(A1, A2)
    assert Appointment._is_conflicting(A2, A1)
    assert not Appointment._is_conflicting(A1, A3)
    assert not Appointment._is_conflicting(A3, A1)
    assert Appointment._is_conflicting(A1, A4)
    assert Appointment._is_conflicting(A4, A1)
    assert Appointment._is_conflicting(A1, A5)
    assert Appointment._is_conflicting(A5, A1)
    assert not Appointment._is_conflicting(A1, A6)
    assert not Appointment._is_conflicting(A6, A1)
    assert Appointment._is_conflicting(A1, A7)
    assert Appointment._is_conflicting(A7, A1)
    assert Appointment._is_conflicting(A1, A8)
    assert Appointment._is_conflicting(A8, A1)

def test___deepcopy__():
    """Test deepcopy for Appointment object."""
    from copy import deepcopy
    name, day, start, end, participants = "a", "Friday", "1:00pm", "2:00pm", [1]
    A = Appointment(name, day, start, end, participants)
    A_copy = deepcopy(A)
    assert A_copy == A
    assert A_copy is not A
    A_copy._name = "lol"
    assert A_copy._name != A._name
    A_copy._day = "lol"
    assert A_copy._day != A._day
    A_copy._start is not A._start
    A_copy._end is not A._end
    A_copy._participants is not A._participants

def test___str__():
    """Test str(Appointment)."""
    name, day, start, end, participants = "a", "Friday", "1:00pm", "2:00pm", [1]
    A1 = Appointment(name, day, start, end, participants)
    assert A1.__str__() == "Appointment \"a\" on Friday from 13:00 to 14:00 with 1"

def test___repr__():
    """Test ."""
    name, day, start, end, participants = "a", "Friday", "1:00pm", "2:00pm", [1]
    A1 = Appointment(name, day, start, end, participants)
    assert A1.__repr__() == "Appointment \"a\" on Friday from 13:00 to 14:00 with 1"
