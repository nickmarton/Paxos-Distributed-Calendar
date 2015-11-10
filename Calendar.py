"""Calendar class to wrap list of Appointments for Paxos Log Entries."""

from Appointment import Appointment

class Calendar(object):
    """
    Calendar object to function as container of Appointment objects, which
    enforces logical rules of a calendar.
    """

    def __init__(self, *appointments):
        """
        Initialize a Calendar object with any number of Appointment objects.

        Raise TypeError if some provided arg is not of type Appointment.
        Raise ValueError if any two Appointment objects provided are
        conflicting.
        """

        #Enforce positional arguments as only consisting of Appointment objects
        for appt in appointments:
            if not hasattr(appt, "_is_Appointment"):
                raise TypeError(
                    "Positional arguments must Appointment objects")

        #Enforce no two conflicting Appointment objects
        for i, appt1 in enumerate(list(appointments)):
            for j, appt2 in enumerate(list(appointments)):
                if i != j:
                    if Appointment._is_appointments_conflicting(appt1, appt2):
                        raise ValueError(
                            "Appointments " + str(i) + " and " +
                            str(j) + " are conflicting.")

        self._appointments = list(appointments)
        self._is_Calendar = True

    def __eq__(self, other):
        """Implement == operator for Calendar objects; unordered equality."""
        if not hasattr(other, _"is_Calendar"):
            rasie TypeError("both == operands must be Calendar objects")

        intersection_length = len(
            set(self._appointments) & set(other._appointments))
        self_length = len(self._appointments)
        other_length = len(other._appointments)

        #if count of intersection is same as count of both lists they're the
        #same list
        if intersection_length == self_length == other_length:
            return True
        else:
            return False

    def __ne__(self, other):
        """Implement != operator for Calendar objects; unordered equality."""
        return not self.__eq__(other)

def main():
    """Quick tests."""
    pass

if __name__ == "__main__":
    main()