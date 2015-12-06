"""Calendar class to wrap list of Appointments for Paxos Log Entries."""

from Appointment import Appointment
import datetime


class Calendar(object):
    """
    Calendar object to function as container of Appointment objects, which
    enforces logical rules of a calendar.

    appointments:               unordered set of Appointment objects; order of
                                addition of appointment objects are tracked
                                however for indexing, i.e.,
                                Calendar[0] == [first appointment added]
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
        if other == None:
            return False

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

    def __iadd__(self, other):
        """
        Implement + operator for Calendar.
        Add an Appointment provided it isn't conflicting.
        """

        appointment_cond = hasattr(other, "_is_Appointment")
        calendar_cond = hasattr(other, "_is_Calendar")

        if not appointment_cond and not calendar_cond:
            raise TypeError(
                "Only Appointment or Calendar objects may be added to a "
                "Calendar object.")

        #handle addition of Appointment
        if appointment_cond:
            if self._is_appointment_conflicting(other):
                raise ValueError(
                    other._name + " is in conflict with Calendar")

            if other not in self:
                self._appointments.append(other)

        #handle addition of Calendar
        if calendar_cond:
            if self._is_calendar_conflicting(other):
                raise ValueError("Cannot add conflicting Calendars")

            for appointment in other:
                if appointment not in self:
                    self._appointments.append(appointment)

        return self

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

    def __deepcopy__(self, memo):
        """Implement copy.deepcopy for Calendar object."""
        from copy import deepcopy
        new_calendar = Calendar()
        for appointment in self:
            new_calendar += deepcopy(appointment)
        return new_calendar

    def _is_appointment_conflicting(self, appointment):
        """
        Determine if Appointment object appointment conflicts with any
        Appointment in Calendar object calendar.

        NOTE: if a copy of appointment is in this Calendar, appointment param
        will not conflict with the copy.
        """

        #Type checking first
        if not hasattr(appointment, "_is_Appointment"):
            raise TypeError(
                "appointment parameter must be an Appointment object")

        #if appointment conflicts with anything in this Calendar
        for calendar_appointment in self:
            if Appointment._is_conflicting(calendar_appointment, appointment):
                return True

        return False

    def _is_calendar_conflicting(self, other):
        """Determine if self and other are conflicting."""

        if not hasattr(other, "_is_Calendar"):
            raise TypeError("both parameters must be Calendar objects.")

        #if any pair of appointments is conflicting, calendars conflict
        for appt1 in self:
            for appt2 in other:
                if Appointment._is_conflicting(appt1, appt2):
                    return True

        return False

    def get_appointment_names(self):
        """Return sorted list of Appointment names in this Calendar object."""
        return sorted([appt._name for appt in self._appointments])

    @staticmethod
    def serialize(calendar):
        """Return a string representation of the calendar with appointments seperated by a hash delimiter"""
        if calendar:
            return "#".join([str(appt) for appt in calendar._appointments])
        else:
            return None

    @staticmethod
    def deserialize(serial_msg):
        """Return a Calendar object parsed from a serialized string"""
        if not serial_msg:
            return None

        appt_list = serial_msg.split("#")
        appt_for_calendar = []
        for appt_str in appt_list:
            
            first_str = appt_str.split(" on ")
            appt_name = first_str[0].split("Appointment ")[1][1:-1]

            second_str = first_str[1].split(" with ")
            user_list = second_str[1].split(" and ")
            users_final = []

            for part in user_list:
                users = part.split(" ")
                for part in users:
                    if len(part) == 2:
                        users_final.append(int(part[:-1]))
                    else:
                        users_final.append(int(part))


            dates_part_1 = first_str[1].split(" from ")
            times = dates_part_1[1].split(" to ")
            start_time = times[0]
            end_time = times[1].split(" with ")[0]
            appointment_day = dates_part_1[0]


            start_time_hour, start_time_minute = [ int(comp_time) for comp_time in start_time.split(":") ]
            end_time_hour, end_time_minute = [ int(comp_time) for comp_time in end_time.split(":")]
            start_time_final = datetime.time(start_time_hour, start_time_minute)
            end_time_final = datetime.time(end_time_hour, end_time_minute)

            appointment = Appointment(appt_name, appointment_day, start_time_final, end_time_final, users_final)
            appt_for_calendar.append(appointment)

        return Calendar(*appt_for_calendar)

    def __str__(self):
        """Implement str(Calendar) ofr Calendar object."""
        ret_str = "Calendar:\n"
        for appointment in sorted(self, key=lambda x: x._name):
            ret_str += '\t' + str(appointment) + '\n'
        return ret_str

    def __repr__(self):
        """Implement repr(Calendar)."""
        return self.__str__()

def main():
    """Quick tests."""
    a1 = Appointment("yo","saturday","12:30pm","1:30pm", [1, 2, 3])
    a3 = Appointment("yo1","saturday","1:30am","12:30pm", [1])
    a4 = Appointment("yo2","sunday","2:30am","12:30pm", [1])
    a5 = Appointment("yo3","monday","12:30am","3:30am", [1])
    a6 = Appointment("yo4","tuesday","4:30am","12:30pm", [1])
    a7 = Appointment("yo5","wednesday","5:30am","12:30pm", [1])
    a8 = Appointment("yo6","thursday","6:30am","12:30pm", [1])
    a9 = Appointment("yo7","friday","7:30am","12:30pm", [1])
    a10 = Appointment("yo8","monday","8:30am","9:30am", [1])
    a11= Appointment("yo9","tuesday","12:30pm","2:30pm", [1])

    c3 = Calendar(a1, a3, a4, a5, a6, a7, a8, a9, a10, a11)
    
    serial_calendar = Calendar.serialize(c3)

    import pickle
    import sys
    msg = pickle.dumps(serial_calendar)
    size = sys.getsizeof(msg)

    print "size", size

    uC = Calendar.deserialize(serial_calendar)

    print c3 == uC
    pass

if __name__ == "__main__":
    main()