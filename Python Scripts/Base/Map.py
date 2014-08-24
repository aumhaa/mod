
"""
Base_Map.py

Created by amounra on 2014-7-26.

This file allows the reassignment of the controls from their default arrangement.  The order is from left to right; 
Buttons are Note #'s and Faders/Rotaries are Controller #'s
"""
OSC_TRANSMIT = False

OSC_OUTPORT = 9001

SHIFT_LATCHING = False

CHANNEL = 0		#main channel (0 - 15)

AFTERTOUCH = True   #when True, sends AT in instrument modes and UserMode.  When false, turns CC's off for instrument modes and transmits CC's in UserModes.

BASE_PADS = [60, 61, 62, 63, 64, 65, 66, 67, 52, 53, 54, 55, 56, 57, 58, 59, 44, 45, 46, 47, 48, 49, 50, 51, 36, 37, 38, 39, 40, 41, 42, 43]	#there are 16 of these

BASE_TOUCHSTRIPS = [1, 2, 3, 4, 5, 6, 7, 8, 9]		#there are 9 of these

BASE_TOUCHPADS = [10, 11, 12, 13, 14, 15, 16, 17]

BASE_BUTTONS = [18, 19, 20, 21, 22, 23, 24, 25]		#there are 16 of these

BASE_RUNNERS = [68, 69, 70, 71, 72, 73, 74, 75]

BASE_LCDS = [34, 35]

COLOR_MAP = [2, 64, 4, 8, 16, 127, 32]

"""This variable determines whether or not the script automatically arms an instruments track for recording when it is selected"""
AUTO_ARM_SELECTED = True

"""This variable determines whether the octave shift for the note offset controls work as momentary or toggle"""
OFFSET_SHIFT_IS_MOMENTARY = False

"""You can change the orientation of the Up, Down, Left, and Right buttons (where applicable) by changing the array.  The values correspond to the buttons from top to bottom."""
UDLR = [0, 1, 2, 3]

"""The values in this array determine the choices for what length of clip is created when "Fixed Length" is turned on:
0 = 1 Beat
1 = 2 Beat
2 = 1 Bar
3 = 2 Bars
4 = 4 Bars
5 = 8 Bars
6 = 16 Bars
7 = 32 Bars
"""


LENGTH_VALUES = [2, 3, 4]


"""The following variables contain color values for different operational mode indicators"""
"""[blackkey, whitekey]"""
KEYCOLORS = [7, 3, 4, 5]
DRUMCOLORS = [4, 6]

CHAN_SELECT = 7

MUTE = 2
SOLO = 3
OFFSET = 6
SHIFT_OFFSET = 13
VERTOFFSET = 7
MIDIMODE = 14
USERMODE = 13
SCALEOFFSET = 5
SPLITMODE = 1
SEQUENCERMODE = 6
DRUMBANK = 7
OVERDUB = 5
RECORD = 6
NEW = 2
LENGTH = 3
SELECTED_NOTE = 6

"""[non-banked, banked]"""
SESSION_NAV = [127, 3]
DEVICE_NAV = 5
BANK_NAV = 4
CHAIN_NAV = 11
DEVICE_LAYER = 12



"""The scale modes and drumpads use the following note maps"""

NOTES = [24, 25, 26, 27, 28, 29, 30, 31, 16, 17, 18, 19, 20, 21, 22, 23, 8, 9, 10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7]
DRUMNOTES = [12, 13, 14, 15, 28, 29, 30, 31, 8, 9, 10, 11, 24, 25, 26, 27, 4, 5, 6, 7, 20, 21, 22, 23, 0, 1, 2, 3, 16, 17, 18, 19]
SCALENOTES = [36, 38, 40, 41, 43, 45, 47, 48, 24, 26, 28, 29, 31, 33, 35, 36, 12, 14, 16, 17, 19, 21, 23, 24, 0, 2, 4, 5, 7, 9, 11, 12]
WHITEKEYS = [0, 2, 4, 5, 7, 9, 11, 12]

"""These are the scales we have available.  You can freely add your own scales to this """
SCALES = 	{'Mod':[0,1,2,3,4,5,6,7,8,9,10,11],
			'Session':[0,1,2,3,4,5,6,7,8,9,10,11],
			'Auto':[0,1,2,3,4,5,6,7,8,9,10,11],
			'Chromatic':[0,1,2,3,4,5,6,7,8,9,10,11],
			'DrumPad':[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],
			'Major':[0,2,4,5,7,9,11],
			'Minor':[0,2,3,5,7,8,10],
			'Dorian':[0,2,3,5,7,9,10],
			'Mixolydian':[0,2,4,5,7,9,10],
			'Lydian':[0,2,4,6,7,9,11],
			'Phrygian':[0,1,3,5,7,8,10],
			'Locrian':[0,1,3,4,7,8,10],
			'Diminished':[0,1,3,4,6,7,9,10],
			'Whole-half':[0,2,3,5,6,8,9,11],
			'Whole_Tone':[0,2,4,6,8,10],
			'Minor_Blues':[0,3,5,6,7,10],
			'Minor_Pentatonic':[0,3,5,7,10],
			'Major_Pentatonic':[0,2,4,7,9],
			'Harmonic_Minor':[0,2,3,5,7,8,11],
			'Melodic_Minor':[0,2,3,5,7,9,11],
			'Dominant_Sus':[0,2,5,7,9,10],
			'Super_Locrian':[0,1,3,4,6,8,10],
			'Neopolitan_Minor':[0,1,3,5,7,8,11],
			'Neopolitan_Major':[0,1,3,5,7,9,11],
			'Enigmatic_Minor':[0,1,3,6,7,10,11],
			'Enigmatic':[0,1,4,6,8,10,11],
			'Composite':[0,1,4,6,7,8,11],
			'Bebop_Locrian':[0,2,3,5,6,8,10,11],
			'Bebop_Dominant':[0,2,4,5,7,9,10,11],
			'Bebop_Major':[0,2,4,5,7,8,9,11],
			'Bhairav':[0,1,4,5,7,8,11],
			'Hungarian_Minor':[0,2,3,6,7,8,11],
			'Minor_Gypsy':[0,1,4,5,7,8,10],
			'Persian':[0,1,4,5,6,8,11],
			'Hirojoshi':[0,2,3,7,8],
			'In-Sen':[0,1,5,7,10],
			'Iwato':[0,1,5,6,10],
			'Kumoi':[0,2,3,7,9],
			'Pelog':[0,1,3,4,7,8],
			'Spanish':[0,1,3,4,5,6,8,10]
			}

SCALEABBREVS = {'Mod':'E3', 'Session':'-S','Auto':'-A','Chromatic':'12','DrumPad':'-D','Major':'M-','Minor':'m-','Dorian':'II','Mixolydian':'V',
			'Lydian':'IV','Phrygian':'IH','Locrian':'VH','Diminished':'d-','Whole-half':'Wh','Whole Tone':'WT','Minor Blues':'mB',
			'Minor Pentatonic':'mP','Major Pentatonic':'MP','Harmonic Minor':'mH','Melodic Minor':'mM','Dominant Sus':'D+','Super Locrian':'SL',
			'Neopolitan Minor':'mN','Neopolitan Major':'MN','Enigmatic Minor':'mE','Enigmatic':'ME','Composite':'Cp','Bebop Locrian':'lB',
			'Bebop Dominant':'DB','Bebop Major':'MB','Bhairav':'Bv','Hungarian Minor':'mH','Minor Gypsy':'mG','Persian':'Pr',
			'Hirojoshi':'Hr','In-Sen':'IS','Iwato':'Iw','Kumoi':'Km','Pelog':'Pg','Spanish':'Sp'}


"""Any scale names in this array will automatically use SplitMode when chosen, regardless of the SplitSwitch for the individual MIDI Channel"""
SPLIT_SCALES = []

"""It is possible to create a custom list of scales to be used by the script.  For instance, the list below would include major, minor, auto, drumpad, and chromatic scales, in that order."""
#SCALENAMES = ['Major', 'Minor', 'Auto', 'DrumPad', 'Chromatic']

"""This is the default scale used by Auto when something other than a drumrack is detected for the selected track"""
DEFAULT_AUTO_SCALE = 'Major'

"""This is the default Vertical Offset for any scale other than DrumPad """
DEFAULT_VERTOFFSET = 4

"""This is the default NoteOffset, aka RootNote, used for scales other than DrumPad"""
DEFAULT_OFFSET = 48

"""This is the default NoteOffset, aka RootNote, used for the DrumPad scale;  it is a multiple of 4, so an offset of 4 is actually a RootNote of 16"""
DEFAULT_DRUMOFFSET = 9

"""This is the default Scale used for all MIDI Channels"""
DEFAULT_SCALE = 'Auto'

"""This is the default SplitMode used for all MIDI Channels"""
DEFAULT_SPLIT = False

from _Framework.ButtonElement import Color
from _Mono_Framework.LividColors import *

class BaseColors:


	class DefaultButton:
		On = LividRGB.WHITE
		Off = LividRGB.OFF
		Disabled = LividRGB.OFF
		Alert = LividRGB.BlinkFast.WHITE
	

	class Session:
		StopClipTriggered = LividRGB.BlinkFast.BLUE
		StopClip = LividRGB.BLUE
		Scene = LividRGB.CYAN
		NoScene = LividRGB.OFF
		SceneTriggered = LividRGB.BlinkFast.BLUE
		ClipTriggeredPlay = LividRGB.BlinkFast.GREEN
		ClipTriggeredRecord = LividRGB.BlinkFast.RED
		RecordButton = LividRGB.OFF
		ClipStopped = LividRGB.WHITE
		ClipStarted = LividRGB.GREEN
		ClipRecording = LividRGB.RED
		NavigationButtonOn = LividRGB.BLUE
	

	class NoteEditor:

		class Step:
			Low = LividRGB.CYAN
			High = LividRGB.WHITE 
			Full = LividRGB.YELLOW
			Muted = LividRGB.YELLOW
			StepEmpty = LividRGB.OFF
		

		class StepEditing:
			High = LividRGB.GREEN
			Low = LividRGB.CYAN
			Full = LividRGB.YELLOW
			Muted = LividRGB.WHITE
		

		StepEmpty = LividRGB.OFF
		StepEmptyBase = LividRGB.OFF
		StepEmptyScale = LividRGB.OFF
		StepDisabled = LividRGB.OFF
		Playhead = Color(31)
		PlayheadRecord = Color(31)
		StepSelected = LividRGB.GREEN
		QuantizationSelected = LividRGB.RED
		QuantizationUnselected = LividRGB.MAGENTA
	

	class LoopSelector:
		Playhead = LividRGB.YELLOW
		OutsideLoop = LividRGB.BLUE
		InsideLoopStartBar = LividRGB.CYAN
		SelectedPage = LividRGB.WHITE
		InsideLoop = LividRGB.CYAN
		PlayheadRecord = LividRGB.RED
	

	class DrumGroup:
		PadAction = LividRGB.WHITE
		PadFilled = LividRGB.GREEN
		PadSelected = LividRGB.WHITE
		PadSelectedNotSoloed = LividRGB.WHITE
		PadEmpty = LividRGB.OFF
		PadMuted = LividRGB.YELLOW
		PadSoloed = LividRGB.CYAN
		PadMutedSelected = LividRGB.BLUE
		PadSoloedSelected = LividRGB.BLUE
		PadInvisible = LividRGB.OFF
		PadAction = LividRGB.RED
	

	class Mixer:
		SoloOn = LividRGB.CYAN
		SoloOff = LividRGB.OFF
		MuteOn = LividRGB.YELLOW
		MuteOff = LividRGB.OFF
		ArmSelected = LividRGB.RED
		ArmUnselected = LividRGB.RED
		ArmOff = LividRGB.OFF
		StopClip = LividRGB.BLUE
	

	class Recording:
		Transition = LividRGB.BlinkSlow.GREEN
	

	class Recorder:
		On = LividRGB.WHITE
		Off = LividRGB.BLUE
		NewOn = LividRGB.BlinkFast.YELLOW
		NewOff = LividRGB.YELLOW
		FixedOn = LividRGB.BlinkFast.CYAN
		FixedOff = LividRGB.CYAN
		RecordOn = LividRGB.BlinkFast.GREEN
		RecordOff = LividRGB.GREEN
		FixedAssigned = LividRGB.MAGENTA
		FixedNotAssigned = LividRGB.OFF
	

	class Transport:
		OverdubOn = LividRGB.BlinkFast.RED
		OverdubOff = LividRGB.RED
	

	class Sequencer:
		OctaveOn = LividRGB.BlinkFast.CYAN
		OctaveOff = LividRGB.OFF
		On = LividRGB.WHITE
		Off = LividRGB.OFF
	

	class Device:
		NavOn = LividRGB.MAGENTA
		NavOff = LividRGB.OFF
		BankOn = LividRGB.YELLOW
		BankOff = LividRGB.OFF
		ChainNavOn = LividRGB.RED
		ChainNavOff = LividRGB.OFF
		ContainNavOn = LividRGB.CYAN
		ContainNavOff = LividRGB.OFF
	

	class Mod:
		
		class Nav:
			OnValue = LividRGB.RED
			OffValue = LividRGB.WHITE
		
	

	class MonoInstrument:

		PressFlash = LividRGB.WHITE
		OffsetOnValue = LividRGB.GREEN
		ScaleOffsetOnValue = LividRGB.RED
		SplitModeOnValue = LividRGB.WHITE
		SequencerModeOnValue = LividRGB.CYAN
		DrumOffsetOnValue = LividRGB.MAGENTA
		VerticalOffsetOnValue = LividRGB.BLUE

		class Keys:
			SelectedNote = LividRGB.GREEN
			RootWhiteValue = LividRGB.RED
			RootBlackValue = LividRGB.MAGENTA
			WhiteValue = LividRGB.CYAN
			BlackValue = LividRGB.BLUE
		

		class Drums:
			SelectedNote = LividRGB.BLUE
			EvenValue = LividRGB.GREEN
			OddValue = LividRGB.MAGENTA
		

	

	class Translation:

		class Channel_10:
			Pad_0 = LividRGB.OFF
			Pad_1 = LividRGB.OFF
			Pad_2 = LividRGB.OFF
			Pad_3 = LividRGB.OFF
			Pad_4 = LividRGB.OFF
			Pad_5 = LividRGB.OFF
			Pad_6 = LividRGB.OFF
			Pad_7 = LividRGB.OFF
			Pad_8 = LividRGB.OFF
			Pad_9 = LividRGB.OFF
			Pad_10 = LividRGB.OFF
			Pad_11 = LividRGB.OFF
			Pad_12 = LividRGB.OFF
			Pad_13 = LividRGB.OFF
			Pad_14 = LividRGB.OFF
			Pad_15 = LividRGB.OFF
			Pad_16 = LividRGB.OFF
			Pad_17 = LividRGB.OFF
			Pad_18 = LividRGB.OFF
			Pad_19 = LividRGB.OFF
			Pad_20 = LividRGB.OFF
			Pad_21 = LividRGB.OFF
			Pad_22 = LividRGB.OFF
			Pad_23 = LividRGB.OFF
			Pad_24 = LividRGB.OFF
			Pad_25 = LividRGB.OFF
			Pad_26 = LividRGB.OFF
			Pad_27 = LividRGB.OFF
			Pad_28 = LividRGB.OFF
			Pad_29 = LividRGB.OFF
			Pad_30 = LividRGB.OFF
			Pad_31 = LividRGB.OFF
		

		class Channel_11:
			Pad_0 = LividRGB.OFF
			Pad_1 = LividRGB.OFF
			Pad_2 = LividRGB.OFF
			Pad_3 = LividRGB.OFF
			Pad_4 = LividRGB.OFF
			Pad_5 = LividRGB.OFF
			Pad_6 = LividRGB.OFF
			Pad_7 = LividRGB.OFF
			Pad_8 = LividRGB.OFF
			Pad_9 = LividRGB.OFF
			Pad_10 = LividRGB.OFF
			Pad_11 = LividRGB.OFF
			Pad_12 = LividRGB.OFF
			Pad_13 = LividRGB.OFF
			Pad_14 = LividRGB.OFF
			Pad_15 = LividRGB.OFF
			Pad_16 = LividRGB.OFF
			Pad_17 = LividRGB.OFF
			Pad_18 = LividRGB.OFF
			Pad_19 = LividRGB.OFF
			Pad_20 = LividRGB.OFF
			Pad_21 = LividRGB.OFF
			Pad_22 = LividRGB.OFF
			Pad_23 = LividRGB.OFF
			Pad_24 = LividRGB.OFF
			Pad_25 = LividRGB.OFF
			Pad_26 = LividRGB.OFF
			Pad_27 = LividRGB.OFF
			Pad_28 = LividRGB.OFF
			Pad_29 = LividRGB.OFF
			Pad_30 = LividRGB.OFF
			Pad_31 = LividRGB.OFF
		

		class Channel_12:
			Pad_0 = LividRGB.OFF
			Pad_1 = LividRGB.OFF
			Pad_2 = LividRGB.OFF
			Pad_3 = LividRGB.OFF
			Pad_4 = LividRGB.OFF
			Pad_5 = LividRGB.OFF
			Pad_6 = LividRGB.OFF
			Pad_7 = LividRGB.OFF
			Pad_8 = LividRGB.OFF
			Pad_9 = LividRGB.OFF
			Pad_10 = LividRGB.OFF
			Pad_11 = LividRGB.OFF
			Pad_12 = LividRGB.OFF
			Pad_13 = LividRGB.OFF
			Pad_14 = LividRGB.OFF
			Pad_15 = LividRGB.OFF
			Pad_16 = LividRGB.OFF
			Pad_17 = LividRGB.OFF
			Pad_18 = LividRGB.OFF
			Pad_19 = LividRGB.OFF
			Pad_20 = LividRGB.OFF
			Pad_21 = LividRGB.OFF
			Pad_22 = LividRGB.OFF
			Pad_23 = LividRGB.OFF
			Pad_24 = LividRGB.OFF
			Pad_25 = LividRGB.OFF
			Pad_26 = LividRGB.OFF
			Pad_27 = LividRGB.OFF
			Pad_28 = LividRGB.OFF
			Pad_29 = LividRGB.OFF
			Pad_30 = LividRGB.OFF
			Pad_31 = LividRGB.OFF
		

		class Channel_13:
			Pad_0 = LividRGB.OFF
			Pad_1 = LividRGB.OFF
			Pad_2 = LividRGB.OFF
			Pad_3 = LividRGB.OFF
			Pad_4 = LividRGB.OFF
			Pad_5 = LividRGB.OFF
			Pad_6 = LividRGB.OFF
			Pad_7 = LividRGB.OFF
			Pad_8 = LividRGB.OFF
			Pad_9 = LividRGB.OFF
			Pad_10 = LividRGB.OFF
			Pad_11 = LividRGB.OFF
			Pad_12 = LividRGB.OFF
			Pad_13 = LividRGB.OFF
			Pad_14 = LividRGB.OFF
			Pad_15 = LividRGB.OFF
			Pad_16 = LividRGB.OFF
			Pad_17 = LividRGB.OFF
			Pad_18 = LividRGB.OFF
			Pad_19 = LividRGB.OFF
			Pad_20 = LividRGB.OFF
			Pad_21 = LividRGB.OFF
			Pad_22 = LividRGB.OFF
			Pad_23 = LividRGB.OFF
			Pad_24 = LividRGB.OFF
			Pad_25 = LividRGB.OFF
			Pad_26 = LividRGB.OFF
			Pad_27 = LividRGB.OFF
			Pad_28 = LividRGB.OFF
			Pad_29 = LividRGB.OFF
			Pad_30 = LividRGB.OFF
			Pad_31 = LividRGB.OFF
		

	








	