from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.CompoundComponent import CompoundComponent
from _Framework.SubjectSlot import SubjectEvent, subject_slot, subject_slot_group

class TranslationComponent(CompoundComponent):


	def __init__(self, controls = [], user_channel_offset = 1, *a, **k):
		super(TranslationComponent, self).__init__()
		self._controls = controls
		self._base_channel = 0
		self._user_channel_offset = user_channel_offset
		self._channel = 0
		self._color = 0
	

	def add_control(self, control):
		if control:
			self._controls.append(control)
	

	def set_channel_selector_buttons(self, buttons):
		self._on_channel_seletor_button_value.subject = buttons
		self.update_channel_selector_buttons()
	

	def update_channel_selector_buttons(self):
		buttons = self._on_channel_seletor_button_value.subject
		if buttons:
			for button, coords in buttons.iterbuttons():
				if button:
					channel = self._channel - self._user_channel_offset
					selected = coords[0] + (coords[1]*buttons.width())
					if channel == selected:
						button.turn_on()
					else:
						button.turn_off()
	

	@subject_slot('value')
	def _on_channel_seletor_button_value(self, value, x, y, *a, **k):
		if value:
			x = x + (y*self._on_channel_seletor_button_value.subject.width())
			self._channel = min(x+self._user_channel_offset, 15)
		self.update()
	

	def update(self):
		if self.is_enabled():
			for control in self._controls:
				control.clear_send_cache()
				control.send_value(self._color, True)
				control.set_channel(self._channel)
				control.set_enabled(False)
		else:
			for control in self._controls:
				control.set_channel(self._base_channel)
				control.set_enabled(True)
		self.update_channel_selector_buttons()
	
