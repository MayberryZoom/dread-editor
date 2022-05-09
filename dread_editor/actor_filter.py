import construct
import imgui


class ActorFilter:
    name_filter: str = ""
    case_sensitive_name: bool = False

    _popup_label: str

    def __init__(self):
        self._popup_label = "Advanced actor filters"

    def draw(self):
        self.name_filter = imgui.input_text("Filter", self.name_filter, 500)[1]
        imgui.same_line()

        if imgui.button(f"More ##{self._popup_label}"):
            imgui.open_popup(self._popup_label)

        if imgui.begin_popup_modal(self._popup_label)[0]:
            self.name_filter = imgui.input_text("Filter", self.name_filter, 500)[1]
            self.case_sensitive_name = imgui.checkbox("Case sensitive search", self.case_sensitive_name)[1]

            if imgui.button(f"Close ##{self._popup_label}"):
                imgui.close_current_popup()

            imgui.end_popup()

    def passes(self, actor: construct.Container) -> bool:
        if not self.name_filter:
            return True

        actor_name: str = actor.sName
        if self.case_sensitive_name:
            actor_name = actor_name.lower()

        for criteria in self.name_filter.split(","):
            criteria = criteria.strip()
            if self.case_sensitive_name:
                criteria = criteria.lower()

            if criteria[0] == "-":
                if criteria[1:] in actor_name:
                    return False
            else:
                if criteria not in actor_name:
                    return False

        return True
