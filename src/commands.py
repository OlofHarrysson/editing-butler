import enum


@enum.unique
class Commands(enum.Enum):
  pass


@enum.unique
class SpeechCommands(Commands):
  wakeword = enum.auto()
  startclip = enum.auto()
  endclip = enum.auto()
  placemarker = enum.auto()
