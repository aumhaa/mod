# by amounra 0714 : http://www.aumhaa.com

from __future__ import with_statement
import Live
import time
import math
import sys

""" _Framework files """
from _Framework.Dependency import inject
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ChannelStripComponent import ChannelStripComponent
from _Framework.ClipSlotComponent import ClipSlotComponent
from _Framework.CompoundComponent import CompoundComponent
from _Framework.ControlElement import ControlElement, ControlElementClient
from _Framework.ControlSurface import ControlSurface
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.DeviceComponent import DeviceComponent
from _Framework.EncoderElement import EncoderElement
from _Framework.InputControlElement import *
from _Framework.MixerComponent import MixerComponent
from _Framework.ModeSelectorComponent import ModeSelectorComponent
from _Framework.NotifyingControlElement import NotifyingControlElement
from _Framework.SceneComponent import SceneComponent
from _Framework.SessionComponent import SessionComponent
from _Framework.SessionZoomingComponent import SessionZoomingComponent  #DeprecatedSessionZoomingComponent as SessionZoomingComponent
from _Framework.SliderElement import SliderElement
from _Framework.TransportComponent import TransportComponent
from _Framework.ModesComponent import DelayMode, CompoundMode, AddLayerMode, LayerMode, MultiEntryMode, ModesComponent, SetAttributeMode, ModeButtonBehaviour, CancellableBehaviour, AlternativeBehaviour, ReenterBehaviour, DynamicBehaviourMixin, ExcludingBehaviourMixin, ImmediateBehaviour, LatchingBehaviour, ModeButtonBehaviour
from _Framework.Layer import Layer
from _Framework.SubjectSlot import SubjectEvent, subject_slot, subject_slot_group
from _Framework.Task import *
from _Framework.M4LInterfaceComponent import M4LInterfaceComponent
from _Framework.ComboElement import ComboElement, DoublePressElement, MultiElement, DoublePressContext
from _Framework.Skin import Skin

"""Imports from the Monomodular Framework"""
from _Mono_Framework.CodecEncoderElement import CodecEncoderElement
from _Mono_Framework.EncoderMatrixElement import NewEncoderMatrixElement as EncoderMatrixElement
from _Mono_Framework.MonoBridgeElement import MonoBridgeElement
from _Mono_Framework.MonoButtonElement import MonoButtonElement
from _Mono_Framework.MonoEncoderElement import MonoEncoderElement
from _Mono_Framework.ResetSendsComponent import ResetSendsComponent
from _Mono_Framework.DetailViewControllerComponent import DetailViewControllerComponent
from _Mono_Framework.DeviceSelectorComponent import NewDeviceSelectorComponent as DeviceSelectorComponent
from _Mono_Framework.MonoDeviceComponent import MonoDeviceComponent
from _Mono_Framework.DeviceNavigator import DeviceNavigator
from _Mono_Framework.LiveUtils import *
from _Mono_Framework.Debug import *
from _Mono_Framework.Mod import *
from _Mono_Framework.LividColors import *
from _Mono_Framework.MonoInstrumentComponent import *
from _Mono_Framework.TranslationComponent import TranslationComponent

debug = initialize_debug()


"""Custom files, overrides, and files from other scripts"""
from _Generic.Devices import *
from ModDevices import *
from Map import *


from Push.AutoArmComponent import AutoArmComponent
from Push.SessionRecordingComponent import *
from Push.ViewControlComponent import ViewControlComponent
from Push.DrumGroupComponent import DrumGroupComponent
from Push.StepSeqComponent import StepSeqComponent
from Push.PlayheadElement import PlayheadElement
from Push.PlayheadComponent import PlayheadComponent
from Push.GridResolution import GridResolution
from Push.ConfigurableButtonElement import ConfigurableButtonElement
from Push.LoopSelectorComponent import LoopSelectorComponent
from Push.Actions import CreateInstrumentTrackComponent, CreateDefaultTrackComponent, CaptureAndInsertSceneComponent, DuplicateDetailClipComponent, DuplicateLoopComponent, SelectComponent, DeleteComponent, DeleteSelectedClipComponent, DeleteSelectedSceneComponent, CreateDeviceComponent
from Push.SelectPlayingClipComponent import SelectPlayingClipComponent

EQ_DEVICES = {'Eq8': {'Gains': [ '%i Gain A' % (index + 1) for index in range(8) ]},
 'FilterEQ3': {'Gains': ['GainHi', 'GainMid', 'GainLo'],
			   'Cuts': ['LowOn', 'MidOn', 'HighOn']}}


check_model = (240, 126, 127, 6, 1, 247)
factoryreset = (240,0,1,97,8,6,247)
SLOWENCODER = (240, 0, 1, 97, 8, 30, 69, 00, 247)
NORMALENCODER = (240, 0, 1, 97, 8, 30, 00, 00, 247)
FASTENCODER = (240, 0, 1, 97, 8, 30, 04, 00, 247)

def release_control(control):
	if control != None:
		control.release_parameter()



class CancellableBehaviourWithRelease(CancellableBehaviour):


	def release_delayed(self, component, mode):
		component.pop_mode(mode)
	

	def update_button(self, component, mode, selected_mode):
		button = component.get_mode_button(mode)
		groups = component.get_mode_groups(mode)
		selected_groups = component.get_mode_groups(selected_mode)
		value = (mode == selected_mode or bool(groups & selected_groups))*32 or 1
		button.send_value(value, True)
	


class ColoredCancellableBehaviourWithRelease(CancellableBehaviourWithRelease):


	def __init__(self, color = 'ButtonDefault.On', off_color = 'ButtonDefault.Off', *a, **k):
		super(ColoredCancellableBehaviourWithRelease, self).__init__(*a, **k)
		self._color = color
		self._off_color = off_color
	

	def update_button(self, component, mode, selected_mode):
		button = component.get_mode_button(mode)
		groups = component.get_mode_groups(mode)
		selected_groups = component.get_mode_groups(selected_mode)
		if mode == selected_mode:
			button.set_light(self._color)
		else:
			button.set_light(self._off_color)
	


class MomentaryBehaviour(ModeButtonBehaviour):


	def press_immediate(self, component, mode):
		component.push_mode(mode)
	

	def release_immediate(self, component, mode):
		if len(component.active_modes) > 1:
			component.pop_mode(mode)
	

	def release_delayed(self, component, mode):
		if len(component.active_modes) > 1:
			component.pop_mode(mode)
	


class BicoloredMomentaryBehaviour(MomentaryBehaviour):


	def __init__(self, color = 'DefaultButton.On', off_color = 'DefaultButton.Off', *a, **k):
		super(BicoloredMomentaryBehaviour, self).__init__(*a, **k)
		self._color = color
		self._off_color = off_color
	

	def update_button(self, component, mode, selected_mode):
		button = component.get_mode_button(mode)
		groups = component.get_mode_groups(mode)
		selected_groups = component.get_mode_groups(selected_mode)
		if mode == selected_mode:
			button.set_light(self._color)
		else:
			button.set_light(self._off_color)
	


class DefaultedBehaviour(ColoredCancellableBehaviourWithRelease):


	def __init__(self, default_mode = 'disabled', *a, **k):
		super(DefaultedBehaviour, self).__init__(*a, **k)
		self._default_mode = default_mode
	

	def press_immediate(self, component, mode):
		if mode is component.selected_mode:
			mode = self._default_mode
		component.push_mode(mode)
	

	def release_immediate(self, component, mode):
		if len(component.active_modes) > 1:
			component.pop_unselected_modes()
	

	def release_delayed(self, component, mode):
		component.pop_mode(mode)
	


class CntrlrSessionRecordingComponent(SessionRecordingComponent):


	def set_new_button(self, button):
		button and button.set_on_off_values('Recorder.NewOn', 'Recorder.NewOff')
		super(CntrlrSessionRecordingComponent, self).set_new_button(button)
	

	def set_record_button(self, button):
		button and button.set_on_off_values('Recorder.RecordOn', 'Recorder.RecordOff')
		super(CntrlrSessionRecordingComponent, self).set_record_button(button)
	

	def set_automation_button(self, button):
		button and button.set_on_off_values('Recorder.AutomationOn', 'Recorder.AutomationOff')
		super(CntrlrSessionRecordingComponent, self).set_automation_button(button)
	


class ShiftModeComponent(ModeSelectorComponent):


	def __init__(self, script, callback, *a, **k):
		super(ShiftModeComponent, self).__init__(*a, **k)
		self._script = script
		self.update = callback
		self._modes_buttons = []
		self._last_mode = 0
		self._set_protected_mode_index(0)
	

	def set_mode_buttons(self, buttons):
		for button in self._modes_buttons:
			button.remove_value_listener(self._mode_value)
		self._modes_buttons = []
		if (buttons != None):
			for button in buttons:
				assert isinstance(button, ButtonElement or FlashingButtonElement)
				identify_sender = True
				button.add_value_listener(self._mode_value, identify_sender)
				self._modes_buttons.append(button)
	

	def number_of_modes(self):
		return 3
	

	def set_mode(self, mode):
		assert isinstance(mode, int)
		mode += 1
		assert (mode in range(self.number_of_modes()))
		if (self._mode_index != mode):
			self._mode_index = mode
			self.update()
		elif (self._mode_index != 0):
			self._mode_index = 0
			self.update()
	

	def _mode_value(self, value, sender):
		assert (len(self._modes_buttons) > 0)
		assert isinstance(value, int)
		assert isinstance(sender, ButtonElement)
		assert (self._modes_buttons.count(sender) == 1)
		if ((value is not 0) or (not sender.is_momentary())):
			self.set_mode(self._modes_buttons.index(sender))
	


class CntrlrResetSendsComponent(ResetSendsComponent):


	def reset_send(self, send_number):
		track = self._script._mixer.channel_strip(send_number)
		for index in range(len(track._send_controls)):
			if track._send_controls[index].mapped_parameter()!=None:
				track._send_controls[index].mapped_parameter().value = 0
	


class CntrlrTransportComponent(TransportComponent):


	def set_record_button(self, button, *a, **k):
		button and button.set_on_off_values('Transport.RecordOn', 'Transport.RecordOff')
		super(CntrlrTransportComponent, self).set_record_button(button, *a, **k)
	

	def set_play_button(self, button, *a, **k):
		button and button.set_on_off_values('Transport.PlayOn', 'Transport.PlayOff')
		super(CntrlrTransportComponent, self).set_play_button(button, *a, **k)
	

	def set_stop_button(self, button, *a, **k):
		button and button.set_on_off_values('Transport.StopOn', 'Transport.StopOn')
		super(CntrlrTransportComponent, self).set_stop_button(button, *a, **k)
	


class CntrlrMixerComponent(MixerComponent):


	def _create_strip(self):
		return CntrlrChannelStripComponent()
	

	def set_next_track_button(self, next_button):
		if next_button is not self._next_track_button:
			self._next_track_button = next_button
			self._next_track_button_slot.subject = next_button
			self.on_selected_track_changed()
	

	def set_previous_track_button(self, prev_button):
		if prev_button is not self._prev_track_button:
			self._prev_track_button = prev_button
			self._prev_track_button_slot.subject = prev_button
			self.on_selected_track_changed()
	

	def set_send_controls(self, controls):
		self._send_controls = controls
		for index, channel_strip in enumerate(self._channel_strips):
			if self.send_index is None:
				channel_strip.set_send_controls([None])
			else:
				send_controls = [ controls.get_button(index, i) for i in xrange(2) ] if controls else [None]
				skipped_sends = [ None for _ in xrange(self.send_index) ]
				channel_strip.set_send_controls(skipped_sends + send_controls)
	

	def set_send_controls(self, controls):
		self._send_controls = controls
		if controls:
			for index in range(len(self._channel_strips)):
				send_controls = [controls.get_button(index, row) for row in range(controls.height())]
				if self.send_index > controls.height:
					send_controls = send_controls + [None for _ in range(self.send_index - controls.height)]
				self._channel_strips[index].set_send_controls(send_controls)
		else:
			for strip in self._channel_strips:
				strip.set_send_controls([None for _ in range(self.send_index)])
	

	def set_return_controls(self, controls):
		for strip, control in map(None, self._return_strips, controls or []):
			strip.set_volume_control(control)
	

	def set_stop_clip_buttons(self, buttons):
		for strip, button in map(None, self._channel_strips, buttons or []):
			strip.set_stop_button(button)
			#debug('set stop button:', button)
	

	def set_eq_gain_controls(self, controls):
		self._eq_controls = controls
		if controls:
			for index in range(len(self._channel_strips)):
				eq_controls = [controls.get_button(index, row) for row in range(controls.height())]
				self._channel_strips[index].set_eq_gain_controls(eq_controls)
		else:
			for strip in self._channel_strips:
				strip.set_eq_gain_controls(None)
	

	def tracks_to_use(self):
		return tuple(self.song().visible_tracks)
	


class CntrlrChannelStripComponent(ChannelStripComponent):


	def __init__(self, *a, **k):
		super(CntrlrChannelStripComponent, self).__init__(*a, **k)
		self._eq_gain_controls = None
		self._eq_device = None
	

	@subject_slot('devices')
	def _on_devices_changed(self):
		debug(self.name, 'on devices changed')
		self._detect_eq(self._track)
		self.update()
	

	def _detect_eq(self, track = None):
		self._eq_device = None
		if not track is None:
			for index in range(len(track.devices)):
				device = track.devices[-1 * (index + 1)]
				if device.class_name in EQ_DEVICES.keys():
					self._eq_device = device
					break
	

	def set_track(self, track):
		assert(isinstance(track, (type(None), Live.Track.Track)))
		self._on_devices_changed.subject = track
		self._detect_eq(track)
		super(CntrlrChannelStripComponent,self).set_track(track)
	

	def set_invert_mute_feedback(self, invert_feedback):
		assert(isinstance(invert_feedback, type(False)))
		self._invert_mute_feedback = invert_feedback
		self.update()
	

	def _on_mute_changed(self):
		if self.is_enabled() and self._mute_button != None:
			if self._track != None or self.empty_color == None:
				if self._track in chain(self.song().tracks, self.song().return_tracks) and self._track.mute != self._invert_mute_feedback:
					self._mute_button.set_light('Mixer.MuteOn')
				else:
					self._mute_button.set_light('Mixer.MuteOff')
			else:
				self._mute_button.set_light(self.empty_color)
	

	def _on_solo_changed(self):
		if self.is_enabled() and self._solo_button != None:
			if self._track != None or self.empty_color == None:
				if self._track in chain(self.song().tracks, self.song().return_tracks) and self._track.solo:
					self._solo_button.set_light('Mixer.SoloOn')
				else:
					self._solo_button.set_light('Mixer.SoloOff')
			else:
				self._solo_button.set_light(self.empty_color)
	

	def _on_arm_changed(self):
		if self.is_enabled() and self._arm_button != None:
			if self._track != None or self.empty_color == None:
				if self._track in self.song().tracks and self._track.can_be_armed and self._track.arm:
					self._arm_button.set_light('Mixer.ArmSelected')
				else:
					self._arm_button.set_light('Mixer.ArmOff')
			else:
				self._arm_button.set_light(self.empty_color)
	

	def set_stop_button(self, button):
		self._on_stop_value.subject = button
		button and button.set_light('Mixer.StopClip')
	

	def on_selected_track_changed(self):
		if self.is_enabled() and self._select_button != None:
			if self._track != None or self.empty_color == None:
				if self.song().view.selected_track == self._track:
					self._select_button.set_light('Mixer.SelectedOn')
				else:
					self._select_button.set_light('Mixer.SelectedOff')
			else:
				self._select_button.set_light(self.empty_color)
	

	@subject_slot('value')
	def _on_stop_value(self, value):
		if self._track:
			self._track.stop_all_clips()
	

	def set_eq_gain_controls(self, controls):
		for control in list(self._eq_gain_controls or []):
			release_control(control)
		self._eq_gain_controls = controls
		self.update()
	

	def _all_controls(self):
		return [self._pan_control, self._volume_control] + list(self._send_controls or []) + list(self._eq_gain_controls or [])
	

	def _connect_parameters(self):
		super(CntrlrChannelStripComponent, self)._connect_parameters()
		if not self._eq_device is None:
			device_dict = EQ_DEVICES[self._eq_device.class_name]
			if self._eq_gain_controls != None:
				gain_names = device_dict['Gains']
				index = 0
				for eq_gain_control in self._eq_gain_controls:
					if eq_gain_control != None:
						if len(gain_names) > index:
							parameter = get_parameter_by_name(self._eq_device, gain_names[index])
							if parameter != None:
								eq_gain_control.connect_to(parameter)
							else:
								eq_gain_control.release_parameter()
								self._empty_control_slots.register_slot(eq_gain_control, nop, 'value')
						else:
							eq_gain_control.release_parameter()
							self._empty_control_slots.register_slot(eq_gain_control, nop, 'value')
					index += 1
	


class CntrlrSessionComponent(SessionComponent):


	def __init__(self, *a, **k):
		super(CntrlrSessionComponent, self).__init__(*a, **k)
		self._vertical_banking.scroll_up_button.color = 'Session.NavigationButtonOn'
		self._vertical_banking.scroll_up_button.disabled_color = 'Session.NavigationButtonOff'
		self._vertical_banking.scroll_down_button.color = 'Session.NavigationButtonOn'
		self._vertical_banking.scroll_down_button.disabled_color = 'Session.NavigationButtonOff'
		self._horizontal_banking.scroll_up_button.color = 'Session.NavigationButtonOn'
		self._horizontal_banking.scroll_up_button.disabled_color = 'Session.NavigationButtonOff'
		self._horizontal_banking.scroll_down_button.color = 'Session.NavigationButtonOn'
		self._horizontal_banking.scroll_down_button.disabled_color = 'Session.NavigationButtonOff'
	

	
class CntrlrM4LInterfaceComponent(ControlSurfaceComponent, ControlElementClient):
	"""
	Simplified API for interaction from M4L as a high priority layer
	superposed on top of any functionality.
	"""


	def __init__(self, controls = None, component_guard = None, priority = 1, *a, **k):
		super(CntrlrM4LInterfaceComponent, self).__init__(self, *a, **k)
		self._priority = priority
		self._controls = dict(map(lambda x: (x.name, x), controls))
		self._grabbed_controls = []
		self._component_guard = component_guard
	

	def disconnect(self):
		for control in self._grabbed_controls[:]:
			self.release_control(control)
		super(CntrlrM4LInterfaceComponent, self).disconnect()
	

	def set_control_element(self, control, grabbed):
		if hasattr(control, 'release_parameter'):
			control.release_parameter()
		control.reset()
	

	def get_control_names(self):
		return self._controls.keys()
	

	def get_control(self, control_name):
		return self._controls[control_name] if control_name in self._controls else None
	

	def grab_control(self, control):
		assert(control in self._controls.values())
		with self._component_guard():
			if control not in self._grabbed_controls:
				control.resource.grab(self, priority=self._priority)
				self._grabbed_controls.append(control)
	

	def release_control(self, control):
		assert(control in self._controls.values())
		with self._component_guard():
			if control in self._grabbed_controls:
				self._grabbed_controls.remove(control)
				control.resource.release(self)
	


class CntrlrMonoInstrumentComponent(MonoInstrumentComponent):


	def _setup_shift_mode(self):
		self._shifted = False
		self._shift_mode = ModesComponent()
		self._shift_mode.add_mode('shift', tuple([self._enable_shift, self._disable_shift]), behaviour = ColoredCancellableBehaviourWithRelease(color = 'MonoInstrument.ShiftOn', off_color = 'MonoInstrument.ShiftOff'))
	


class Cntrlr(ControlSurface):
	__module__ = __name__
	__doc__ = " Monomodular controller script for Livid CNTRLR "


	def __init__(self, *a, **k):
		super(Cntrlr, self).__init__(*a, **k)
		self._version_check = 'b996'
		self._host_name = 'Cntrlr'
		self._color_type = 'OhmRGB'
		self._client = [None for index in range(4)]
		self._active_client = None
		self._rgb = 0
		self._timer = 0
		self._touched = 0
		self.flash_status = 1
		self._skin = Skin(CntrlrColors)
		self._device_selection_follows_track_selection = FOLLOW
		with self.component_guard():
			self._setup_monobridge()
			self._setup_controls()
			self._setup_transport_control()
			self._setup_autoarm()
			self._setup_session_recording_component()
			self._setup_mixer_control()
			self._setup_send_resets()
			self._setup_session_control()
			self._setup_device_control()
			self._setup_device_selector()
			self._setup_translations()
			self._setup_viewcontrol()
			self._setup_mod()
			self._setup_instrument()
			self._setup_modswitcher()
			self._setup_modes() 
			self._setup_m4l_interface()
			self._on_device_changed.subject = self.song()
			self.set_feedback_channels(range(14, 15))
		self._main_modes.selected_mode = 'MixMode'
		self.schedule_message(1, self._open_log)
	

	def _open_log(self):
		self.log_message("<<<<<<<<<<<<<<<<<<<<= " + str(self._host_name) + " " + str(self._version_check) + " log opened =>>>>>>>>>>>>>>>>>>>") 
		self.show_message(str(self._host_name) + ' Control Surface Loaded')
	

	def _setup_monobridge(self):
		self._monobridge = MonoBridgeElement(self)
		self._monobridge.name = 'MonoBridge'
	

	def _setup_controls(self):
		is_momentary = True	
		self._fader = [MonoEncoderElement(MIDI_CC_TYPE, CHANNEL, CNTRLR_FADERS[index], Live.MidiMap.MapMode.absolute, 'Fader_' + str(index), index, self) for index in range(8)]
		self._dial_left = [MonoEncoderElement(MIDI_CC_TYPE, CHANNEL, CNTRLR_KNOBS_LEFT[index], Live.MidiMap.MapMode.absolute, 'Dial_Left_' + str(index), CNTRLR_KNOBS_LEFT[index], self) for index in range(12)]
		self._dial_right = [MonoEncoderElement(MIDI_CC_TYPE, CHANNEL, CNTRLR_KNOBS_RIGHT[index], Live.MidiMap.MapMode.absolute, 'Dial_Right_' + str(index), CNTRLR_KNOBS_RIGHT[index], self) for index in range(12)]
		self._encoder = [CodecEncoderElement(MIDI_CC_TYPE, CHANNEL, CNTRLR_DIALS[index], Live.MidiMap.MapMode.absolute, 'Encoder_' + str(index), CNTRLR_DIALS[index], self) for index in range(12)]	
		self._encoder_button = [MonoButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, CNTRLR_DIAL_BUTTONS[index], 'Encoder_Button_' + str(index), self, skin = self._skin) for index in range(12)]	
		self._grid = [MonoButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, CNTRLR_GRID[index], 'Grid' + str(index), self, skin = self._skin) for index in range(16)]
		self._button = [MonoButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, CNTRLR_BUTTONS[index], 'Button_' + str(index), self, skin = self._skin) for index in range(32)]
		self._knobs = self._dial_left + self._dial_right

		self._fader_matrix = ButtonMatrixElement(name = 'Fader_Matrix', rows = [self._fader])
		self._matrix = ButtonMatrixElement(name = 'Matrix', rows = [self._grid[index*4:(index*4)+4] for index in range(4)])
		self._knob_left_matrix = ButtonMatrixElement(name = 'Knob_Left_Matrix', rows = [self._dial_left[index*4:(index*4)+4] for index in range(3)])
		self._knob_right_matrix = ButtonMatrixElement(name = 'Knob_Right_Matrix', rows = [self._dial_right[index*4:(index*4)+4] for index in range(3)])
		self._dial_matrix = ButtonMatrixElement(name = 'Dial_Matrix', rows = [self._encoder[index*4:(index*4)+4] for index in range(3)])
		self._dial_button_matrix = ButtonMatrixElement(name = 'Dial_Button_Matrix', rows = [self._encoder_button[index*4:(index*4)+4] for index in range(1,3)])
		self._key_matrix = ButtonMatrixElement(name = 'Key_Matrix', rows = [self._button[0:16], self._button[16:32]])
		
		self._translated_controls = self._fader + self._knobs + self._encoder[4:] + self._encoder_button[4:] + self._grid + self._button
	

	def _setup_transport_control(self):
		self._transport = CntrlrTransportComponent() 
		self._transport.name = 'Transport'
		self._transport.layer = Layer(priority = 4,
									play_button = self._button[28],
									record_button = self._button[30],
									stop_button = self._button[29])
	

	def _setup_autoarm(self):
		self._auto_arm = AutoArmComponent(name='Auto_Arm')
		self._auto_arm.can_auto_arm_track = self._can_auto_arm_track
	

	def _setup_session_recording_component(self):
		self._clip_creator = ClipCreator()
		self._clip_creator.name = 'ClipCreator'
		self._recorder = CntrlrSessionRecordingComponent(self._clip_creator, ViewControlComponent()) # is_enabled = False)
		self._recorder.layer = Layer(priority = 4, new_button = self._button[28], record_button = self._button[29], automation_button = self._button[30])
		self._recorder.set_enabled(False)
	

	def _setup_mixer_control(self):
		is_momentary = True
		self._num_tracks = (4)
		self._mixer = CntrlrMixerComponent(4, num_returns = 2, name = 'Mixer', auto_name = True, invert_mute_feedback = True)
		self._mixer.set_track_offset(0)
		if self._mixer.channel_strip(0)._track:
			self.song().view.selected_track = self._mixer.channel_strip(0)._track
		self._mixer.main_faders_layer = AddLayerMode(self._mixer, Layer(priority = 4,
											volume_controls = self._fader_matrix.submatrix[:4, :],
											return_controls = self._fader_matrix.submatrix[4:6, :],
											prehear_volume_control = self._fader[6],))
		self._mixer.main_buttons_layer = AddLayerMode(self._mixer, Layer(priority = 4, 
											mute_buttons = self._key_matrix.submatrix[:4, 1:],
											arm_buttons = self._key_matrix.submatrix[4:8, :1],
											solo_buttons = self._key_matrix.submatrix[:4, :1],
											track_select_buttons = self._key_matrix.submatrix[4:8, 1:],))
		self._mixer.stop_layer = AddLayerMode(self._mixer, Layer(priority = 4,
											stop_clip_buttons = self._key_matrix.submatrix[8:12, 1:],))
		self._mixer.main_knobs_layer = AddLayerMode(self._mixer, Layer(priority = 4,
											send_controls = self._knob_left_matrix.submatrix[:, :2],
											pan_controls = self._knob_left_matrix.submatrix[:, 2:],
											eq_gain_controls = self._knob_right_matrix))
		self._mixer.master_fader_layer = AddLayerMode(self._mixer.master_strip(), Layer(priority = 4,
											volume_control = self._fader[7]))
		self._mixer.instrument_buttons_layer = AddLayerMode(self._mixer, Layer(priority = 4,
											mute_buttons = self._key_matrix.submatrix[:4, 1:],
											track_select_buttons = self._key_matrix.submatrix[4:8, 1:],))
	

	def _setup_send_resets(self):
		self._send_reset = CntrlrResetSendsComponent(self)
		self._send_reset.name = 'Sends_Reset'
		self._send_reset.layer = Layer(buttons = self._key_matrix.submatrix[8:12, :1])
	

	def _setup_session_control(self):
		self._session = CntrlrSessionComponent(num_tracks = 4, num_scenes = 4, name = 'Session', enable_skinning = True, auto_name = True)
		self._session.set_mixer(self._mixer)
		self.set_highlighting_session_component(self._session)
		self._session.layer = Layer(priority = 4, clip_launch_buttons = self._matrix)
		self._session.nav_layer = AddLayerMode(self._session, Layer(priority = 4,
									scene_bank_down_button = self._button[14],
									scene_bank_up_button = self._button[15],
									track_bank_left_button = self._button[12],
									track_bank_right_button = self._button[13]))

		self._session_zoom = SessionZoomingComponent(session = self._session, name = 'Session_Overview', enable_skinning = True)  # is_enabled = False)  #
		self._session_zoom.buttons_layer = AddLayerMode(self._session_zoom, Layer(priority = 4, button_matrix = self._matrix))

		self._session.set_offsets(0, 0)
	

	def _setup_device_control(self):
		self._device_selection_follows_track_selection = FOLLOW
		self._device = DeviceComponent()
		self._device.name = 'Device_Component'
		self._device._is_banking_enabled = self.device_is_banking_enabled(self._device)
		self.set_device_component(self._device)
		self._device.layer = Layer(priority = 4, parameter_controls = self._dial_matrix.submatrix[:, 1:3], 
											lock_button = self._encoder_button[5],
											on_off_button = self._encoder_button[4],
											bank_prev_button = self._encoder_button[6],
											bank_next_button = self._encoder_button[7])

		self._device_navigator = DeviceNavigator(self._device, self._mixer, self)
		self._device_navigator.name = 'Device_Navigator'
		self._device_navigator.layer = Layer(priority = 4, prev_button = self._encoder_button[8], 
											next_button = self._encoder_button[9], 
											prev_chain_button = self._encoder_button[10], 
											next_chain_button = self._encoder_button[11],)
	

	def _setup_device_selector(self):
		self._device_selector = DeviceSelectorComponent(self)  # is_enabled = False)
		self._device_selector.name = 'Device_Selector'
		self._device_selector.layer = Layer(matrix = self._matrix)
		self._device_selector.set_enabled(False)
	

	def _setup_translations(self):
		self._translations = TranslationComponent(self._translated_controls, 4)  # is_enabled = False)
		self._translations.name = 'TranslationComponent'
		self._translations._channel = 4
		self._translations.layer = Layer(priority = 10,)
		self._translations.selector_layer = AddLayerMode(self._translations, Layer(channel_selector_control = self._encoder[3]))
		self._translations.set_enabled(False)
	

	def _setup_mod(self):
		self.monomodular = get_monomodular(self)
		self.monomodular.name = 'monomodular_switcher'
		self.modhandler = CntrlrModHandler(self) # is_enabled = False)
		self.modhandler.name = 'ModHandler' 
		self.modhandler.set_lock_button(self._encoder_button[1])
		self.modhandler.layer = Layer(priority = 8, cntrlr_encoder_grid = self._dial_matrix,
										cntrlr_encoder_button_grid = self._dial_button_matrix,
										cntrlr_grid = self._matrix,
										cntrlr_keys = self._key_matrix,)
										#parameter_controls = self._dial_matrix)
	

	def _setup_instrument(self):
		self._grid_resolution = self.register_disconnectable(GridResolution())
		self._c_instance.playhead.enabled = True
		self._playhead_element = PlayheadElement(self._c_instance.playhead)
		self._playhead_element.reset()

		self._instrument = CntrlrMonoInstrumentComponent(self, self._skin, grid_resolution = self._grid_resolution, name = 'InstrumentModes') # is_enabled = False)
		#self._instrument.layer = Layer(priority = 10, shift_mode_button = self._button[31])
		self._instrument.shift_button_layer = AddLayerMode(self._instrument, Layer(priority = 5, shift_mode_button = self._button[31]))
		self._instrument.audioloop_layer = LayerMode(self._instrument, Layer(priority = 4, loop_selector_matrix = self._key_matrix.submatrix[:, :1]))
		self._instrument.keypad_shift_layer = AddLayerMode(self._instrument, Layer(priority = 4, 
									scale_up_button = self._button[13], 
									scale_down_button = self._button[12],
									offset_up_button = self._button[11], 
									offset_down_button = self._button[10],
									vertical_offset_up_button = self._button[9],
									vertical_offset_down_button = self._button[8],
									split_button = self._button[14],
									sequencer_button = self._button[15]))
		self._instrument.drumpad_shift_layer = AddLayerMode(self._instrument, Layer(priority = 4, 
									scale_up_button = self._button[13],
									scale_down_button = self._button[12],
									drum_offset_up_button = self._button[11], 
									drum_offset_down_button = self._button[10],
									drumpad_mute_button = self._button[9],
									drumpad_solo_button = self._button[8],
									split_button = self._button[14],
									sequencer_button = self._button[15]))
		self._instrument._keypad.main_layer = LayerMode(self._instrument._keypad, Layer(priority = 4, keypad_matrix = self._matrix))
		self._instrument._keypad.sequencer_layer = LayerMode(self._instrument._keypad, Layer(priority = 4, playhead = self._playhead_element, keypad_matrix = self._matrix, sequencer_matrix = self._key_matrix.submatrix[:,:1]))
		self._instrument._keypad.split_layer = LayerMode(self._instrument._keypad, Layer(priority = 4, keypad_matrix = self._matrix, split_matrix = self._key_matrix.submatrix[:8,:1]))
		self._instrument._keypad.sequencer_shift_layer = LayerMode(self._instrument._keypad, Layer(priority = 4, keypad_matrix = self._matrix, loop_selector_matrix = self._key_matrix.submatrix[:8, :1], quantization_buttons = self._key_matrix.submatrix[:7, 1:], follow_button = self._button[23]))
		self._instrument._drumpad.main_layer = LayerMode(self._instrument._drumpad, Layer(priority = 4, drumpad_matrix = self._matrix))
		self._instrument._drumpad.sequencer_layer = LayerMode(self._instrument._drumpad, Layer(priority = 4, playhead = self._playhead_element, drumpad_matrix = self._matrix, sequencer_matrix = self._key_matrix.submatrix[:,:1]))
		self._instrument._drumpad.split_layer = LayerMode(self._instrument._drumpad, Layer(priority = 4, drumpad_matrix = self._matrix, split_matrix = self._key_matrix.submatrix[:8,:1]))
		self._instrument._drumpad.sequencer_shift_layer = LayerMode(self._instrument._drumpad, Layer(priority = 4, drumpad_matrix = self._matrix, loop_selector_matrix = self._key_matrix.submatrix[:8, :1], quantization_buttons = self._key_matrix.submatrix[:7, 1:], follow_button = self._button[23]))
		self._instrument.set_enabled(False)
	

	def _setup_modswitcher(self):
		self._modswitcher = ModesComponent(name = 'ModSwitcher')  # is_enabled = False)
		self._modswitcher.add_mode('mod', [self.modhandler])
		self._modswitcher.add_mode('instrument', [self._instrument, self._instrument.shift_button_layer])
		self._modswitcher.set_enabled(False)
	

	def _setup_viewcontrol(self):
		self._view_control = ViewControlComponent(name='View_Control')# is_enabled = False)
		self._view_control.layer = Layer(prev_track_button=self._button[24], next_track_button= self._button[25], next_scene_button=self._button[27], prev_scene_button = self._button[26])
		self._view_control.set_enabled(False)
	

	def _setup_modes(self):
		main_buttons=CompoundMode(self._mixer.main_buttons_layer, self._mixer.stop_layer, self._transport, self._send_reset, self._session.nav_layer)
		main_buttons_instrument=CompoundMode(self._mixer.main_buttons_layer, self._recorder, self._view_control)
		main_faders=CompoundMode(self._mixer.main_faders_layer, self._mixer.master_fader_layer)
		bottom_buttons=CompoundMode(self._mixer.instrument_buttons_layer, self._recorder, self._view_control)

		self._instrument._main_modes = ModesComponent(name = 'InstrumentModes')
		self._instrument._main_modes.add_mode('disabled', [main_buttons_instrument, main_faders, self._mixer.main_knobs_layer, self._device, self._session, self._recorder, self._view_control, self._send_reset, self._session.nav_layer])
		self._instrument._main_modes.add_mode('drumpad', [self._instrument._drumpad.main_layer, main_buttons_instrument, self._send_reset, self._session.nav_layer])
		self._instrument._main_modes.add_mode('drumpad_split', [self._instrument._drumpad.split_layer, self._send_reset, self._session.nav_layer])
		self._instrument._main_modes.add_mode('drumpad_sequencer', [self._instrument._drumpad.sequencer_layer, bottom_buttons])
		self._instrument._main_modes.add_mode('drumpad_shifted', [self._instrument._drumpad.main_layer, self._instrument.drumpad_shift_layer, main_buttons_instrument, self._recorder, self._view_control])
		self._instrument._main_modes.add_mode('drumpad_split_shifted', [self._instrument._drumpad.split_layer, self._instrument.drumpad_shift_layer, bottom_buttons, self._recorder, self._view_control])
		self._instrument._main_modes.add_mode('drumpad_sequencer_shifted', [self._instrument._drumpad.sequencer_shift_layer, self._instrument.drumpad_shift_layer, self._recorder, self._view_control])
		self._instrument._main_modes.add_mode('keypad', [self._instrument._keypad.main_layer, main_buttons_instrument, self._send_reset, self._session.nav_layer])
		self._instrument._main_modes.add_mode('keypad_split', [self._instrument._keypad.split_layer, bottom_buttons, self._send_reset, self._session.nav_layer])
		self._instrument._main_modes.add_mode('keypad_sequencer', [self._instrument._keypad.sequencer_layer, bottom_buttons])
		self._instrument._main_modes.add_mode('keypad_shifted', [self._instrument._keypad.main_layer, self._instrument.keypad_shift_layer, main_buttons_instrument, self._recorder, self._view_control])
		self._instrument._main_modes.add_mode('keypad_split_shifted', [self._instrument._keypad.split_layer, self._instrument.keypad_shift_layer, bottom_buttons, self._recorder, self._view_control])
		self._instrument._main_modes.add_mode('keypad_sequencer_shifted', [self._instrument._keypad.sequencer_shift_layer, self._instrument.keypad_shift_layer, self._recorder, self._view_control])
		self._instrument._main_modes.add_mode('audioloop', [self._instrument.audioloop_layer, self._session, bottom_buttons, self._recorder, self._view_control])
		self._instrument.register_component(self._instrument._main_modes)
		self._instrument.set_enabled(False)

		self._session_modes = ModesComponent(name = 'SessionModes', is_enabled = False)
		self._session_modes.add_mode('Session', [self._session])
		self._session_modes.add_mode('SessionZoom', [self._session_zoom.buttons_layer], behaviour = BicoloredMomentaryBehaviour(color = 'Session.ZoomOn', off_color = 'Session.ZoomOff'))
		self._session_modes.layer = Layer(priority = 4, SessionZoom_button = self._button[31])
		self._session_modes.selected_mode = 'Session'

		self._main_modes = ModesComponent(name = 'MainModes')
		self._main_modes.add_mode('MixMode', [main_buttons, main_faders, self._mixer.main_knobs_layer, self._device, self._session_modes, self._session.nav_layer])
		self._main_modes.add_mode('ModSwitcher', [self._modswitcher, main_faders, self._mixer.main_knobs_layer], behaviour = DefaultedBehaviour(default_mode = 'MixMode', color = 'ModeButtons.ModSwitcher', off_color = 'ModeButtons.ModSwitcherDisabled'))
		self._main_modes.add_mode('Translations', [self._translations, DelayMode(self._translations.selector_layer), main_faders, self._mixer.main_knobs_layer], behaviour = DefaultedBehaviour(default_mode = 'MixMode', color = 'ModeButtons.Translations', off_color = 'ModeButtons.TranslationsDisabled'))
		self._main_modes.add_mode('DeviceSelector', [self._device_selector, main_buttons, main_faders, self._mixer.main_knobs_layer, self._device], behaviour = ColoredCancellableBehaviourWithRelease(color = 'ModeButtons.DeviceSelector', off_color = 'ModeButtons.DeviceSelectorDisabled'))
		self._main_modes.layer = Layer(priority = 4, ModSwitcher_button = self._encoder_button[0], Translations_button = self._encoder_button[3], DeviceSelector_button = self._encoder_button[2])
	

	def _setup_m4l_interface(self):
		self._m4l_interface = CntrlrM4LInterfaceComponent(controls=self.controls, component_guard=self.component_guard, priority = 10)
		self._m4l_interface.name = "M4LInterface"
		self.get_control_names = self._m4l_interface.get_control_names
		self.get_control = self._m4l_interface.get_control
		self.grab_control = self._m4l_interface.grab_control
		self.release_control = self._m4l_interface.release_control
	

	def _can_auto_arm_track(self, track):
		routing = track.current_input_routing
		return routing == 'Ext: All Ins' or routing == 'All Ins' or routing.startswith('Base Input')
	

	@subject_slot('appointed_device')
	def _on_device_changed(self):
		debug('appointed device changed, script')
		self.schedule_message(2, self._update_modswitcher)
	

	def _on_selected_track_changed(self):
		super(Cntrlr, self)._on_selected_track_changed()
		self.schedule_message(2, self._update_modswitcher)
	

	def _update_modswitcher(self):
		debug('update modswitcher', self.modhandler.active_mod())
		if self.modhandler.active_mod():
			self._modswitcher.selected_mode = 'mod'
		else:
			self._modswitcher.selected_mode = 'instrument'
	

	def reset_controlled_track(self, track = None, *a):
		if not track:
			track = self.song().view.selected_track
		self.set_controlled_track(track)
	

	def set_controlled_track(self, track = None, *a):
		if isinstance(track, Live.Track.Track):
			super(Cntrlr, self).set_controlled_track(track)
		else:
			self.release_controlled_track()
	

	"""called on timer"""
	def update_display(self):
		super(Cntrlr, self).update_display()		#since we are overriding this from the inherited method, we need to call the original routine as well
		self._timer = (self._timer + 1) % 256	#each 100/60ms, increase the self._timer property by one.  Start over at 0 when we hit 256
		self.modhandler.send_ring_leds()	#if local rings are turned off, then we need to send the new values if they've changed			
		self.flash()							#call the flash method below
	

	def flash(self):
		if(self.flash_status > 0):
			for control in self.controls:
				if isinstance(control, MonoButtonElement):
					control.flash(self._timer)		
	

	"""m4l lcd bridge"""
	def generate_strip_string(self, display_string):
		NUM_CHARS_PER_DISPLAY_STRIP = 12
		if (not display_string):
			return (' ' * NUM_CHARS_PER_DISPLAY_STRIP)
		if ((len(display_string.strip()) > (NUM_CHARS_PER_DISPLAY_STRIP - 1)) and (display_string.endswith('dB') and (display_string.find('.') != -1))):
			display_string = display_string[:-2]
		if (len(display_string) > (NUM_CHARS_PER_DISPLAY_STRIP - 1)):
			for um in [' ',
			 'i',
			 'o',
			 'u',
			 'e',
			 'a']:
				while ((len(display_string) > (NUM_CHARS_PER_DISPLAY_STRIP - 1)) and (display_string.rfind(um, 1) != -1)):
					um_pos = display_string.rfind(um, 1)
					display_string = (display_string[:um_pos] + display_string[(um_pos + 1):])
		else:
			display_string = display_string.center((NUM_CHARS_PER_DISPLAY_STRIP - 1))
		ret = u''
		for i in range((NUM_CHARS_PER_DISPLAY_STRIP - 1)):
			if ((ord(display_string[i]) > 127) or (ord(display_string[i]) < 0)):
				ret += ' '
			else:
				ret += display_string[i]

		ret += ' '
		ret = ret.replace(' ', '_')
		assert (len(ret) == NUM_CHARS_PER_DISPLAY_STRIP)
		return ret
	

	def notification_to_bridge(self, name, value, sender):
		if(isinstance(sender, (MonoEncoderElement, CodecEncoderElement))):
			pn = str(self.generate_strip_string(name))
			pv = str(self.generate_strip_string(value))
			self._monobridge._send(sender.name, 'lcd_name', pn)
			self._monobridge._send(sender.name, 'lcd_value', pv)
	

	def touched(self):
		if self._touched is 0:
			self._monobridge._send('touch', 'on')
			self.schedule_message(2, self.check_touch)
		self._touched +=1
	

	def check_touch(self):
		if self._touched > 5:
			self._touched = 5
		elif self._touched > 0:
			self._touched -= 1
		if self._touched is 0:
			self._monobridge._send('touch', 'off')
		else:
			self.schedule_message(2, self.check_touch)
	

	def handle_sysex(self, midi_bytes):
		pass
	

	def disconnect(self):
		self.log_message("<<<<<<<<<<<<<<<<<<<<<<<<< " + str(self._host_name) + " log closed >>>>>>>>>>>>>>>>>>>>>>>>>")
		super(Cntrlr, self).disconnect()
	

	def restart_monomodular(self):
		#debug('restart monomodular')
		self.modhandler.disconnect()
		with self.component_guard():
			self._setup_mod()
	

	def _get_num_tracks(self):
		return self.num_tracks
	

	"""a closure fix for banking when we deassign the bank buttons and still want to change bank indexes"""
	def device_is_banking_enabled(self, device):
		def _is_banking_enabled():
			return True
		return _is_banking_enabled
		
	


class CntrlrModHandler(ModHandler):


	def __init__(self, *a, **k):
		self._local = True
		self._last_sent_leds = 1
		self._cntrlr_grid = None
		self._cntrlr_encoder_grid = None
		self._cntrlr_keys = None
		addresses = {'cntrlr_grid': {'obj':Grid('cntrlr_grid', 4, 4), 'method':self._receive_cntrlr_grid},
					'cntrlr_encoder_grid': {'obj':RingedGrid('cntrlr_encoder_grid', 4, 3), 'method':self._receive_cntrlr_encoder_grid},
					'cntrlr_encoder_button_grid': {'obj':Grid('cntrlr_encoder_button_grid', 4, 2), 'method':self._receive_cntrlr_encoder_button_grid},
					'cntrlr_key': {'obj':  Grid('cntrlr_key', 16, 2), 'method': self._receive_cntrlr_key}}
		super(CntrlrModHandler, self).__init__(addresses = addresses, *a, **k)
		self._color_type = 'RGB'
		self.nav_box = self.register_component(NavigationBox(self, 16, 16, 4, 4, self.set_offset))

	

	def _receive_cntrlr_grid(self, x, y, value, *a, **k):
		#self.log_message('_receive_cntrlr_grid: %(x)s %(y)s %(value)s ' % {'x':x, 'y':y, 'value':value})
		if self.is_enabled() and self._active_mod and not self._active_mod.legacy and not self._cntrlr_grid is None and x < 4 and y < 4:
			self._cntrlr_grid.send_value(x, y, self._colors[value], True)
	

	def _receive_cntrlr_encoder_grid(self, x, y, *a, **k):
		#self.log_message('_receive_cntrlr_encoder_grid: %(x)s %(y)s %(k)s' % {'x':x, 'y':y, 'k':k})
		if self.is_enabled() and self._active_mod and not self._cntrlr_encoder_grid is None and x < 4 and y < 3:
			keys = k.keys()
			if 'value' in keys:
				if self._local:
					self._cntrlr_encoder_grid.send_value(x, y, k['value'], True)
				else:
					self._cntrlr_encoder_grid.get_button(x, y)._ring_value = k['value']
			if 'mode' in keys:
				self._cntrlr_encoder_grid.get_button(x, y).set_mode(k['mode'])
			if 'green' in keys:
				self._cntrlr_encoder_grid.get_button(x, y).set_green(k['green'])
			if 'custom' in keys:
				self._cntrlr_encoder_grid.get_button(x, y).set_custom(k['custom'])
			if 'local' in keys:
				self._receive_cntrlr_encoder_grid_local(k['local'])
			if 'relative' in keys:
				self._receive_cntrlr_encoder_grid_relative(k['relative'])
	

	def _receive_cntrlr_encoder_button_grid(self, x, y, value, *a, **k):
		if self.is_enabled() and self._active_mod:
			if not self._cntrlr_encoder_button_grid is None:
				self._cntrlr_encoder_button_grid.send_value(x, y, self._colors[value], True)
	

	def _receive_cntrlr_encoder_grid_relative(self, value, *a):
		#self.log_message('_receive_cntrlr_encoder_grid_relative: %(v)s' % {'v':value})
		if self.is_enabled() and self._active_mod:
			value and self._script._send_midi(tuple([240, 0, 1, 97, 8, 17, 127, 127, 127, 127, 127, 127, 127, 127, 247])) or self._script._send_midi(tuple([240, 0, 1, 97, 8, 17, 0, 0, 0, 0, 0, 0, 0, 0, 247]))
	

	def _receive_cntrlr_encoder_grid_local(self, value, *a):
		#self.log_message('_receive_cntrlr_encoder_grid_local: %(v)s' % {'v':value})
		if self.is_enabled() and self._active_mod:
			self.clear_rings()
			self._local = value
			value and self._script._send_midi(tuple([240, 0, 1, 97, 8, 8, 72, 247])) or self._script._send_midi(tuple([240, 0, 1, 97, 8, 8, 64, 247]))
	

	def _receive_cntrlr_key(self, x, y=0, value=0, *a):
		#self.log_message('_receive_cntrlr_key: %(x)s %(y)s %(value)s ' % {'x':x, 'y':y, 'value':value})
		if self.is_enabled() and self._active_mod and not self._active_mod.legacy:
			if not self._cntrlr_keys is None:
				self._cntrlr_keys.send_value(x, y, self._colors[value], True)
	

	def _receive_grid(self, x, y, value, *a, **k):
		if self.is_enabled() and self._active_mod and self._active_mod.legacy:
			if not self._cntrlr_grid is None:
				if (x - self.x_offset) in range(4) and (y - self.y_offset) in range(4):
					self._cntrlr_grid.send_value(x - self.x_offset, y - self.y_offset, self._colors[value], True)
	


	def set_cntrlr_grid(self, grid):
		self._cntrlr_grid = grid
		self._cntrlr_grid_value.subject = self._cntrlr_grid
	

	def set_cntrlr_encoder_grid(self, grid):
		self._cntrlr_encoder_grid = grid
		#self._cntrlr_encoder_grid_value.subject = self._cntrlr_encoder_grid
		self.set_parameter_controls(grid)
		self.log_message('parameter controls are: ' + str(self._parameter_controls))
	

	def set_cntrlr_encoder_button_grid(self, buttons):
		self._cntrlr_encoder_button_grid = buttons
		self._cntrlr_encoder_button_grid_value.subject = self._cntrlr_encoder_button_grid
	

	def set_cntrlr_keys(self, keys):
		self._cntrlr_keys = keys
		#if keys:
		#	for key in keys.iterbuttons():
		#		key and key.send_value(0, True)
		self._cntrlr_keys_value.subject = self._cntrlr_keys
	


	@subject_slot('value')
	def _cntrlr_keys_value(self, value, x, y, *a, **k):
		#self.log_message('_cntrlr_keys_value: %(x)s %(y)s %(value)s ' % {'x':x, 'y':y, 'value':value})
		if self._active_mod:
			self._active_mod.send('cntrlr_key', x, y, value)
	

	@subject_slot('value')
	def _cntrlr_grid_value(self, value, x, y, *a, **k):
		#self.log_message('_cntrlr_grid_value: %(x)s %(y)s %(value)s ' % {'x':x, 'y':y, 'value':value})
		if self._active_mod:
			if self._active_mod.legacy:
				self._active_mod.send('grid', x + self.x_offset, y + self.y_offset, value)
			else:
				self._active_mod.send('cntrlr_grid', x, y, value)
	

	@subject_slot('value')
	def _cntrlr_encoder_grid_value(self, value, x, y, *a, **k):
		#self.log_message('_cntrlr_encoder_grid_value: %(x)s %(y)s %(value)s ' % {'x':x, 'y':y, 'value':value})
		if self._active_mod:
			self._active_mod.send('cntrlr_encoder_grid', x, y, value)
	

	@subject_slot('value')
	def _cntrlr_encoder_button_grid_value(self, value, x, y, *a, **k):
		#self.log_message('_cntrlr_encoder_button_grid_value: %(x)s %(y)s %(value)s ' % {'x':x, 'y':y, 'value':value})
		if self._active_mod:
			self._active_mod.send('cntrlr_encoder_button_grid', x, y, value)
	


	@subject_slot('appointed_device')
	def _on_device_changed(self):
		super(CntrlrModHandler, self)._on_device_changed()
		self._script._on_device_changed()
	

	def select_mod(self, *a, **k):
		super(CntrlrModHandler, self).select_mod(*a, **k)
		self._script._on_device_changed()
	

	def update(self, *a, **k):
		mod = self.active_mod()
		#self.log_message('modhandler update: ' + str(mod))
		if self.is_enabled() and not mod is None:
			mod.restore()
		else:
			#debug('disabling modhandler')
			self._script._send_midi(tuple([240, 0, 1, 97, 8, 17, 0, 0, 0, 0, 0, 0, 0, 0, 247]))
			self._script._send_midi(tuple([240, 0, 1, 97, 8, 8, 72, 247]))
			if not self._cntrlr_grid_value.subject is None:
				self._cntrlr_grid_value.subject.reset()
			if not self._cntrlr_encoder_grid_value.subject is None:
				self._cntrlr_encoder_grid_value.subject.reset()
			if not self._cntrlr_encoder_button_grid_value.subject is None:
				self._cntrlr_encoder_button_grid_value.subject.reset()
			if not self._cntrlr_keys_value.subject is None:
				self._cntrlr_keys_value.subject.reset()
		if not self._on_lock_value.subject is None:
			self._on_lock_value.subject.send_value((not mod is None) + ((not mod is None) and self.is_locked() * 4))
	

	def send_ring_leds(self):
		if self.is_enabled() and self._active_mod and not self._local and self._cntrlr_encoder_grid:
			leds = [240, 0, 1, 97, 8, 31]
			for encoder, coords in self._cntrlr_encoder_grid.iterbuttons():
				bytes = encoder._get_ring()
				leds.append(bytes[0])
				leds.append(int(bytes[1]) + int(bytes[2]))
			leds.append(247)
			if not leds==self._last_sent_leds:
				self._script._send_midi(tuple(leds))
				self._last_sent_leds = leds
	

	def clear_rings(self):
		self._last_sent_leds = 1
	

#	a