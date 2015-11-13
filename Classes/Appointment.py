"""
Appointment class for Distributed Calendar implemented with Paxos Algorithm.
"""

from datetime import time

class Appointment(object):
    """
    Appointment class.

    name:           name of the appointment enforced as a string.
    day:            day of the appointment enforced as a string
                    matching some day of the week.
    start:          start time of the appointment enforced as a string of the
                    form (digit){1,2}:(digit){2}(am|pm).
    end:            end time of the appointment enforced as a string of the
                    form (digit){1,2}:(digit){2}(am|pm).
    participants:   list of participants in the appointment.
    """

    def __init__(self, name, day, start_time, end_time, participants):
        """Initialize an Appointment object."""
        #enforce name and day as strings
        if not isinstance(name, str):
            raise TypeError("name parameter must be of type string.")
        if not isinstance(day, str):
            raise TypeError("day parameter must be of type string.")

        days = ["sunday", "monday", "tuesday", "wednesday", "thursday",
        "friday", "saturday"]

        #enforce day as a valid day of the week
        if day.lower() not in days:
            raise ValueError("day parameter must be a day of the week.")

        start = Appointment._parse_time(start_time)
        end = Appointment._parse_time(end_time)

        if not (start < end):
            raise ValueError(
                "start_time parameter must come strictly before end_time "
                "parameter.")

        if not isinstance(participants, list):
            raise TypeError(
                "participants parameter must be of type list")

        for participant in participants:
            if not isinstance(participant, int):
                raise TypeError(
                    "participants parameter must contain only node_id ints")

        if not participants:
            raise ValueError("There must be at least 1 participant")

        self._name = name
        self._day = day[0].upper() + day[1:].lower()
        self._start = start
        self._end = end
        self._participants = participants
        self._is_Appointment = True

    def __eq__(self, other):
        """Determine if two Appointment objects are equivalent."""
        if not hasattr(other, "_is_Appointment"):
            raise TypeError("both operands must be Appointment objects.")

        c_name = self._name == other._name
        c_day = self._day == other._day
        c_start = self._start == other._start
        c_end = self._end == other._end
        
        #if the length of the union of the participants is equal to the length
        #of the intersection, they are the same participants
        intersection = set(self._participants) & set(other._participants)
        union = set(self._participants) | set(other._participants)
        c_participants = len(union) == len(intersection)

        return c_name and c_day and c_start and c_end and c_participants

    def __ne__(self, other):
        """Determine if two Appointment objects are not equivalent."""
        return not self.__eq__(other)

    def _key(self):
        """Key for Appointment hashing; simple tuple."""
        return (self._name, self._day, self._start, self._end,
                                            tuple(self._participants))

    def __hash__(self):
        """Hash Appointment object; used so we can call set(Appointment)."""
        return hash(self._key())

    @staticmethod
    def _parse_time(time_string):
        """Return a time object from given string or raise exception."""
        #enforce string type
        if not type(time_string) == str:
            raise TypeError("time parameters must be of type string.")

        #regex to determine if times provided are in correct format,
        #i.e., [digit][digit]:[digit][digit](am|pm)
        import re
        pattern = r"\d{1,2}:\d\d(am|pm)"
        if not re.match(pattern, time_string):
            raise ValueError(
                "time parameters must be of form "
                "(digit){1,2}:(digit){2}(am|pm)..")

        #split hour, minutes, and merediem from string
        hour, minutes = time_string[:-2].split(":")
        meridiem = time_string[-2:]

        hour = int(hour)
        minutes = int(minutes)
        
        #ensure hour and minutes are correct
        if hour < 0 or hour > 12:
            raise ValueError(
                "hour digits must be between 0 and 12.")

        if minutes % 30 != 0:
            raise ValueError("minute digits must be 00 or 30.")

        #convert hour to military time via meridiem
        if meridiem == "pm" and hour != 12:
            hour += 12

        if meridiem == "am":
            hour %= 12

        if meridiem != "am" and meridiem != "pm":
            raise ValueError("meridiem must be 'am' or 'pm'")

        #return time object
        return time(hour, minutes)

    @staticmethod
    def _is_conflicting(appt1, appt2):
        """Determine if two Appointment objects are conflicting."""
        #ensure both args are of type Appointment
        appt1_cond = hasattr(appt1, "_is_Appointment")
        appt2_cond = hasattr(appt2, "_is_Appointment")

        if not appt1_cond or not appt2_cond:
            raise TypeError("parameters must be of type Appointment")

        #if they're the same appointment, they don't conflict
        if appt1 == appt2:
            return False

        #if appointments aren't on the same day, they don't conflict
        if appt1._day != appt2._day:
            return False

        #if there are no overlapping participants, they are not in conflict
        if not set(appt1._participants) & set(appt2._participants):
            return False

        #grab time objects from Appointment object
        start1, end1 = appt1._start, appt1._end
        start2, end2 = appt2._start, appt2._end

        #handle [s1,e1][s2,e2]
        if end1 <= start2:
            return False

        #handle [s2,e2][s1,e1]
        if end2 <= start1:
            return False

        #if there's any overlap, they are in conflict
        return True

    def __str__(self):
        """Convert event object to human readable string representation."""
        #add name
        appointment_str = "Appointment \"" + self._name + "\" on "
        #add day
        appointment_str += self._day[0].upper() + self._day[1:] + " from "
        #add time
        appointment_str += str(self._start)[:-3] + " to " + str(self._end)[:-3]
        appointment_str += " with "
        #add participants
        if len(self._participants) > 2:
            appointment_str += "".join(
                [str(i) + ", " for i in self._participants[:-1]])
            appointment_str += "and " + str(self._participants[-1])
        elif len(self._participants) == 2:
            appointment_str += str(self._participants[0]) + " and "
            appointment_str += str(self._participants[1])
        else:
            appointment_str += str(self._participants[0])

        return appointment_str

    def __repr__(self):
        """Convert event object to machine representation."""
        return self.__str__()

def main():
    """Method for testing; not executed unless 'usr$ python Appointment.py'."""

    a1 = Appointment("yo","saturday","12:30pm","1:30pm", [1, 2, 3])
    a2 = Appointment("yerboi","saturday","1:30am","11:30pm", [1, 4, 5])
    a3 = Appointment("we out here","saturday","11:30am","12:30pm", [1])

    print a1.__repr__()

if __name__ == "__main__":
    main()

