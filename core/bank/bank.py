class Bank():
    def __init__(self):
        self._amount = 0
        self._chain = [20, 50, 100, 200, 300, 450, 600, 800, 1000]
        self._current_pos = 0

    def increment(self):
        if self._current_pos < len(self._chain) - 1:
            self._current_pos += 1

    @property
    def current_pos(self):
        return self._current_pos

    @current_pos.setter
    def current_pos(self, pos:int):
        self._current_pos = pos

    def reset_chain(self):
        self._current_pos = 0

    def save(self)->int:
        amount_saved = self._chain[self._current_pos]
        self._amount += amount_saved
        self.reset_chain()
        return amount_saved

    def __str__(self):
        return_str = f'| $ {self._amount} |'
        for i in range(len(self._chain)):
            return_str = f'{return_str} [{self._chain[self._current_pos]}]' if i == self._current_pos else f'{return_str} {self._chain[i]}'
        return_str = return_str + " |"
        return return_str