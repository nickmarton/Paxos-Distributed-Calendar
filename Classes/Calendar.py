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
                    if Appointment._is_conflicting(appt1, appt2):
                        raise ValueError(
                            "Appointments \n" + str(appt1) + "\n and \n" +
                            str(appt2) + "\n are conflicting.")

        #remove duplicates and set
        l_appointments = list(appointments)
        self._appointments = []

        #loop through with list instead of set to keep order
        for appointment in l_appointments:
            if appointment not in self._appointments:
                self._appointments.append(appointment)

        self._is_Calendar = True

    def __eq__(self, other):
        """Implement == operator for Calendar objects; unordered equality."""
        if not hasattr(other, "_is_Calendar"):
            raise TypeError("both == operands must be Calendar objects")

        intersection_length = len(
            set(self._appointments) & set(other._appointments))
        union_length = len(set(self._appointments) | set(other._appointments))

        #if count of intersection is same as count of both lists they're the
        #same list
        if intersection_length == union_length:
            return True
        else:
            return False

    def __ne__(self, other):
        """Implement != operator for Calendar objects; unordered equality."""
        return not self.__eq__(other)

    def __len__(self):
        """Implement len(Calendar)."""
        return len(self._appointments)

    def __getitem__(self, key):
        """Implement indexing for Calendar object."""
        try:
            return self._appointments[key]
        except TypeError:
            raise TypeError("Index must be an int")
        except IndexError:
            raise IndexError("invalid index: " + str(key))

    def __setitem__(self, key, value):
        """
        Implement Calendar[key] = value; needed to ensure no conflicts added.
        """

        if not hasattr(value, "_is_Appointment"):
            raise TypeError("value parameter must be an Appointment object")

        #Ensure valid key while setting
        try:
            self._appointments[key]
        except TypeError:
            raise TypeError("Index must be an int")
        except IndexError:
            raise IndexError("invalid index: " + str(key))

        non_key_appts = []
        for i, appt in enumerate(self._appointments):
            if i != key:
                non_key_appts.append(appt)

        for appt in non_key_appts:
            if Appointment._is_conflicting(value, appt):
                raise ValueError(
                    str(value) + "\n conflicts with \n" + str(appt) +
                    "\n already in Calendar")
        
        for appt in non_key_appts:
            if value == appt:
                raise ValueError(
                    "Cannot add duplicate Appointment to Calendar")

        self._appointments[key] = value

    def __iter__(self):
        """Implement iterator for Calendar."""
        for appointment in self._appointments:
            yield appointment

    def __contains__(self, item):
        """Implement "in" operator for Calendar object."""
        for appointment in self:
            if appointment == item:
                return True

        return False

    @staticmethod
    def _is_appointment_conflicting(calendar, appointment):
        """
        Determine if Appointment object appointment conflicts with any
        Appointment in Calendar object calendar.
        """

        #Type checking first
        if not hasattr(appointment, "_is_Appointment"):
            raise TypeError(
                "appointment parameter must be an Appointment object")

        #if appointment conflicts with anything in this Calendar
        for calendar_appointment in calendar:
            if Appointment.is_conflicting(
                calendar_appointment, appointment):
                return True

        return False

    @staticmethod
    def _is_calendar_conflicting(calendar1, calendar2):
        """Determine if calendar1 and calendar2 are conflicting."""

        c1_cond = has_attr(calendar1, "_is_Calendar")
        c2_cond = has_attr(calendar2, "_is_Calendar")

        #if either parameter is not a calendar, raise TypeError
        if not c1_cond or not c2_cond:
            raise TypeError("both parameters must be Calendar objects.")

        #if any pair of appointments is conflicting, calendars conflict
        for appt1 in calendar1:
            for appt2 in calendar2:
                if Appointment._is_conflicting(appt1, appt2):
                    return True

        return False

    def add(self, appointment):
        """
        Implement add for Calendar; add an Appointment provided it isn't
        conflicting.
        """

        if Calendar._is_appointment_conflicting(self, appointment):
            raise ValueError(
                appointment._name + " is in conflict with Calendar")

        if appointment not in self:
            self._appointments.append(appointment)

def main():
    """Quick tests."""
    pass

if __name__ == "__main__":
    main()