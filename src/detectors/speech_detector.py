from collections import namedtuple, defaultdict
from abc import ABC

from src.fake_data import get_fake_words
from src.commands import SpeechCommands as SpeechCmd
from .transcriber import Transcriber


class SpeechRecognizer(ABC):
  def __init__(self, commandword_bias):
    self.commandword_bias = commandword_bias
    command_format = namedtuple('Command', 'command command_variant')
    self.commands = []
    self.commands.append(command_format(SpeechCmd.wakeword, 'butler'))
    self.commands.append(command_format(SpeechCmd.startclip, 'start clip'))
    self.commands.append(command_format(SpeechCmd.endclip, 'end clip'))
    self.commands.append(command_format(SpeechCmd.endclip, 'stop clip'))
    self.commands.append(command_format(SpeechCmd.placemarker, 'add markers'))
    self.commands.append(command_format(SpeechCmd.placemarker, 'add marker'))

  def transcribe_audio(audio):
    ''' Implemented in subclass '''
    raise NotImplementedError

  def find_actions(self, audio, fake_data):
    if fake_data:
      transcriber = Transcriber([])
      transcriber.words = get_fake_words()
    else:
      raw_words = self.transcribe_audio(audio)
      transcriber = Transcriber(raw_words)

    print(f"\nButler heard: {transcriber.transcription}\n\n")
    words = transcriber.format_transcription(self.commands)

    index2word = {i: w for i, w in enumerate(words)}
    command2index = defaultdict(list)
    for ind, word in index2word.items():
      if isinstance(word.text, SpeechCmd):
        command2index[word.text].append(ind)

    to_timestring = lambda x: f'{int(x*1000)}/1000'  # TODO: Problem?

    actions = defaultdict(list)
    for wake_word_ind in command2index[SpeechCmd.wakeword]:
      command_word = index2word[wake_word_ind + 1]

      if command_word.text == SpeechCmd.placemarker:
        marker_word = index2word[wake_word_ind + 2]
        action = dict(time=to_timestring(marker_word.start_time),
                      name=marker_word.text)
        actions[command_word.text].append(action)

      if command_word.text == SpeechCmd.startclip:
        action = dict(time=command_word.start_time)
        actions[command_word.text].append(action)

      if command_word.text == SpeechCmd.endclip:
        action = dict(time=command_word.end_time)
        actions[command_word.text].append(action)

    # TODO: Try to match uneven lengths of start/end
    formated_actions = defaultdict(list)
    for start_clip, end_clip in zip(actions[SpeechCmd.startclip],
                                    actions[SpeechCmd.endclip]):
      action = dict(start_time=to_timestring(start_clip['time']),
                    end_time=to_timestring(end_clip['time']),
                    duration=to_timestring(end_clip['time'] -
                                           start_clip['time']))
      formated_actions['clips'].append(action)

    formated_actions['markers'] = actions[SpeechCmd.placemarker]
    return dict(formated_actions)
