from collections import namedtuple
from src.commands import SpeechCommands  # Needed for the eval


class Transcriber():
  def __init__(self, raw_words):
    self.word_format = namedtuple('Word', 'text start_time end_time')

    self.words = []
    for word in raw_words:
      start_time = word.start_time.seconds + word.start_time.nanos / 1e9
      end_time = word.end_time.seconds + word.end_time.nanos / 1e9
      self.words.append(self.word_format(word.word, start_time, end_time))
      # TODO: Add confidence?

  def format_transcription(self, commands):
    placeholder = '!placeholder!'
    text = ' '.join([w.text for w in self.words])
    text = text.lower()

    for command, command_alternative in commands:
      n_words_command = len(command_alternative.split())
      placeh = " ".join([placeholder for _ in range(n_words_command - 1)])
      text = text.replace(command_alternative, f'{command} {placeh}')
    text = text.split()

    assert len(self.words) == len(text)

    formated_words = []
    for w, t in zip(self.words, text):
      if t != placeholder:
        if t.startswith('SpeechCommands.'):
          t = eval(t)

        formated_words.append(self.word_format(t, w.start_time, w.end_time))

    return formated_words

  @property
  def transcription(self):
    text = [w.text for w in self.words]
    return ' '.join(text)
