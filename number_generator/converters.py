
class SixDigitConverter:
    regex = "[0-9]{6}"

    def to_python(self, value):
        return int(value)
    
    def to_url(self, value):
        return "%06d" % value
