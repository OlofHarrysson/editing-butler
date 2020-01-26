from collections import namedtuple


def get_fake_words():
  words = 'hej video helper start clip video helper end clip nothatspodracing video helper add marker poop what video helper start clip hej det är test video helper end clip this is another video helper add marker mymarker test stop this'.split(
  )
  Word = namedtuple('Word', 'text start_time end_time')
  words = [Word(w, 0, 1) for w in words]
  # return words

  words = [
    Word(text='hello', start_time=1.0, end_time=1.3),
    Word(text='this', start_time=1.3, end_time=1.6),
    Word(text='is', start_time=1.6, end_time=1.7),
    Word(text='the', start_time=1.7, end_time=1.8),
    Word(text='second', start_time=1.8, end_time=2.1),
    Word(text='test', start_time=2.1, end_time=2.4),
    Word(text='of', start_time=2.4, end_time=2.5),
    Word(text='my', start_time=2.5, end_time=2.6),
    Word(text='tool', start_time=2.6, end_time=3.1),
    Word(text='videohelper', start_time=4.1, end_time=4.4),
    Word(text='start', start_time=4.4, end_time=5.8),
    Word(text='clip', start_time=5.8, end_time=6.3),
    Word(text='videohelper', start_time=11.8, end_time=14.5),
    Word(text='stop', start_time=14.5, end_time=16.0),
    Word(text='clip', start_time=16.0, end_time=16.3),
    Word(text='videohelper', start_time=20.1, end_time=20.4),
    Word(text='add', start_time=22.7, end_time=23.2),
    Word(text='markers', start_time=23.2, end_time=24.0),
    Word(text='scooter', start_time=25.4, end_time=26.3),
    Word(text='car', start_time=27.1, end_time=27.8),
    Word(text='winter', start_time=28.9, end_time=29.7),
    Word(text='house', start_time=30.0, end_time=30.8),
    Word(text='videohelper', start_time=32.3, end_time=34.6),
    Word(text='add', start_time=34.6, end_time=36.7),
    Word(text='markers', start_time=36.7, end_time=37.6),
    Word(text='car', start_time=39.2, end_time=40.0),
    Word(text='street', start_time=40.5, end_time=40.9),
    Word(text='sign', start_time=40.9, end_time=41.5),
    Word(text='walking', start_time=42.0, end_time=42.8),
    Word(text='videohelper', start_time=45.9, end_time=46.6),
    Word(text='start', start_time=46.6, end_time=48.1),
    Word(text='clip', start_time=48.1, end_time=48.4),
    Word(text='videohelper', start_time=54.0, end_time=54.3),
    Word(text='stop', start_time=54.3, end_time=56.3),
    Word(text='clip', start_time=56.3, end_time=56.6),
    Word(text='videohelper', start_time=62.6, end_time=63.8),
    Word(text='add', start_time=63.8, end_time=64.9),
    Word(text='marker', start_time=64.9, end_time=65.5),
    Word(text='sunni-shia', start_time=65.5, end_time=66.9),
    Word(text="that's", start_time=66.9, end_time=67.8),
    Word(text='a', start_time=67.8, end_time=67.8),
    Word(text='bad', start_time=67.8, end_time=68.1),
    Word(text='one', start_time=68.1, end_time=68.2),
    Word(text='actually', start_time=68.2, end_time=68.6),
    Word(text='because', start_time=68.6, end_time=68.7),
    Word(text="it's", start_time=68.7, end_time=69.0),
    Word(text='not', start_time=69.0, end_time=69.3),
    Word(text='a', start_time=69.3, end_time=69.4),
    Word(text='word', start_time=69.4, end_time=69.4),
    Word(text='videohelper', start_time=71.3, end_time=75.1),
    Word(text='add', start_time=75.1, end_time=76.3),
    Word(text='marker', start_time=76.3, end_time=76.8),
    Word(text='flag', start_time=76.8, end_time=77.4),
    Word(text='Pope', start_time=77.4, end_time=77.9)
  ]

  return words