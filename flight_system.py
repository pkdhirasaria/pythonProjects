class Flight:

    def __init__(self, number, aircraft):
        self._number = number
        self._aircraft = aircraft

        rows, seats = self._aircraft.seating_plan()
        self._seating = [None] + [{letter: None for letter in seats} for _ in rows]

    def number(self):
        return self._number

    def airline(self):
        return self._number[:2]

    def aircraft_model(self):
        return  self._aircraft.model()

    def _validate_seat(self, seat):
        """
        :param seat: accept seat number and validate it
        :return: tuples of seat row and column
        """
        rows, seating_letter = self._aircraft.seating_plan()
        letter = seat[-1]

        if letter not in seating_letter:
            raise ValueError("Invalid Seat Letter {}".format(letter))

        row_text = seat[:-1]
        try:
            row = int(row_text)
        except ValueError:
            raise ValueError("Invalid Seat Row {}".format(row_text))

        if row not in rows:
            raise ValueError("Invalid row number {}".format(row))

        return row, letter

    def allocate_seat(self, seat, passenger):

        row, letter = self._validate_seat(seat)
        if self._seating[row][letter] is not None:
            raise ValueError("Seat {} already occupied".format(seat))
        self._seating[row][letter] = passenger

    def relocate_passenger_method(self, old_seat, new_seat):
        """

        :param old_seat: old seat at which passenger is assigned
        :param new_seat: new seat at which passenger want to get assigned
        """
        row, letter = self._validate_seat(old_seat)

        if self._seating[row][letter] is None:
            raise ValueError("Seat {} is unoccupied".format(old_seat))

        to_row, to_letter = self._validate_seat(new_seat)
        if self._seating[to_row][to_letter] is not None:
            raise ValueError("Seat {} already occupied".format(new_seat))
        passenger = self._seating[row][letter]
        self._seating[row][letter] = None

        self._seating[to_row][to_letter] = passenger

    def num_available_seat(self):
        """
        :return: number of available seats
        """
        return sum(sum(1 for s in rows.values() if s is None)
                   for rows in self._seating if rows is not None)

    def boarding_information(self):
        for passenger, seat in sorted(self._passenger_information()):
            _boarding_pass_printer(passenger, seat, self.number(), self.aircraft_model())

    def _passenger_information(self):

        rows, letters = self._aircraft.seating_plan()
        for row in rows:
            for letter in letters:
                passenger = self._seating[row][letter]
                if passenger is not None:
                    yield (passenger, "{}{}".format(row, letter))


class Aircraft:

    def __init__(self, registration, model, num_rows, num_seats_per_row):
        self._registration = registration
        self._model = model
        self._num_rows = num_rows
        self._num_seats_per_row = num_seats_per_row

    def registration(self):
        return self._registration

    def model(self):
        return self._model

    def seating_plan(self):
        return range(1, self._num_rows + 1), "ABCDEFGHJK"[:self._num_seats_per_row]


def make_model():
    f = Flight("SN0601", Aircraft("G-868", "Airbus 319", 22, 7))
    f.allocate_seat("5A", "Light Yagami")
    f.allocate_seat("1A", "Magnus Carlsen")
    f.allocate_seat("3A", "Boby Ficher")
    f.allocate_seat("5D", "Vishy Anand")

    return f


def _boarding_pass_printer(passenger, seat, flight_num, model):

    output = "| Name: {0}"   \
             " Seat: {1}"     \
             " Flight Number: {2}" \
             " Aircraft: {3} |".format(passenger, seat, flight_num, model)

    border = '+' + '-' * (len(output) - 2) + '+'
    banner = '|' + ' ' * (len(output) - 2) + '|'
    line = [border, banner, output, banner, border]
    card = '\n'.join(line)
    print(card)
    print()
