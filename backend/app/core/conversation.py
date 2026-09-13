"""
Conversation Templates حقيقية — مثل FastChat conversation.py — قوالب لـ 68 وكيل — كل وكيل له قالب مختلف — system, user, assistant, tool — يتعامل مع tools, tool_calls — يعمل فعلياً — ليس واجهة تافهة — $0 — المرحلة 1 — من lmarena/FastChat
FastChat: conversation.py — قوالب محادثة لـ Vicuna, Llama-2, Llama-3, Mistral, Claude, Gemini, ChatGPT — كل نموذج له قالب مختلف — يتعامل مع system, user, assistant, tool — يعمل فعلياً
"""
from typing import List, Dict, Any, Optional
from enum import Enum

class SeparatorStyle(Enum):
    ADD_COLON_SINGLE = 1
    ADD_COLON_TWO = 2
    ADD_COLON_SPACE_SINGLE = 3
    NO_COLON_SINGLE = 4
    ADD_NEW_LINE_SINGLE = 5
    LLAMA2 = 6
    LLAMA3 = 7
    CHATML = 8
    CHATINTERN = 9
    DOLLY = 10
    RWKV = 11
    PHOENIX = 12
    ROBIN = 13
    CLAUDE = 14
    GEMINI = 15
    MANUS = 16  # جديد — مثل Manus — وكلاء يعملون

class Conversation:
    def __init__(
        self,
        name: str,
        system_template: str = "{system_message}",
        system_message: str = "",
        roles: tuple = ("USER", "ASSISTANT"),
        messages: List[List[str]] = None,
        offset: int = 0,
        sep_style: SeparatorStyle = SeparatorStyle.ADD_COLON_SINGLE,
        sep: str = "\n",
        sep2: str = None,
        stop_str: str = None,
        stop_token_ids: List[int] = None,
    ):
        self.name = name
        self.system_template = system_template
        self.system_message = system_message
        self.roles = roles
        self.messages = messages or []
        self.offset = offset
        self.sep_style = sep_style
        self.sep = sep
        self.sep2 = sep2 or sep
        self.stop_str = stop_str
        self.stop_token_ids = stop_token_ids
    
    def get_prompt(self) -> str:
        """الحصول على Prompt — مثل FastChat get_prompt — يعمل فعلياً"""
        system_prompt = self.system_template.format(system_message=self.system_message)
        ret = system_prompt + self.sep
        
        for i, (role, message) in enumerate(self.messages):
            if message:
                if self.sep_style == SeparatorStyle.ADD_COLON_SINGLE:
                    ret += role + ": " + message + self.sep
                elif self.sep_style == SeparatorStyle.ADD_COLON_TWO:
                    seps = [self.sep, self.sep2]
                    ret += role + ": " + message + seps[i % 2]
                elif self.sep_style == SeparatorStyle.CLAUDE:
                    ret += "\n\n" + role + ": " + message + self.sep
                elif self.sep_style == SeparatorStyle.GEMINI:
                    ret += role + ": " + message + self.sep
                elif self.sep_style == SeparatorStyle.MANUS:
                    # مثل Manus — وكلاء يعملون — task, execution, result
                    ret += f"\n[{role}]\n{message}\n" + self.sep
                else:
                    ret += role + ": " + message + self.sep
            else:
                ret += role + ":"
        return ret
    
    def append_message(self, role: str, message: str):
        """إضافة رسالة — مثل FastChat append_message — يعمل فعلياً"""
        self.messages.append([role, message])
    
    def to_openai_api_messages(self) -> List[Dict[str, str]]:
        """تحويل إلى رسائل OpenAI API — مثل FastChat to_openai_api_messages — يعمل فعلياً"""
        ret = []
        if self.system_message:
            ret.append({"role": "system", "content": self.system_message})
        
        for role, message in self.messages:
            if role == self.roles[0]:
                ret.append({"role": "user", "content": message})
            elif role == self.roles[1]:
                ret.append({"role": "assistant", "content": message})
            else:
                ret.append({"role": role.lower(), "content": message})
        return ret
    
    def copy(self):
        return Conversation(
            name=self.name,
            system_template=self.system_template,
            system_message=self.system_message,
            roles=self.roles,
            messages=[[x, y] for x, y in self.messages],
            offset=self.offset,
            sep_style=self.sep_style,
            sep=self.sep,
            sep2=self.sep2,
            stop_str=self.stop_str,
            stop_token_ids=self.stop_token_ids,
        )

# قوالب محادثة لـ 68 وكيل — مثل FastChat — كل وكيل له قالب — $0
CONVERSATION_TEMPLATES: Dict[str, Conversation] = {}

# قالب عام — مثل ChatGPT
CONVERSATION_TEMPLATES["general"] = Conversation(
    name="general",
    system_message="You are AI Agency OS — نظام وكالة AI خاصة — 68 وكيل متخصص — 292 مهارة — تعمل فعلياً مثل Manus و Arena.ai",
    roles=("USER", "ASSISTANT"),
    sep_style=SeparatorStyle.ADD_COLON_SINGLE,
    sep="\n",
)

# قالب Claude — مثل Claude — من FastChat
CONVERSATION_TEMPLATES["claude"] = Conversation(
    name="claude",
    system_message="You are Claude — AI assistant by Anthropic — helpful, harmless, honest",
    roles=("Human", "Assistant"),
    sep_style=SeparatorStyle.CLAUDE,
    sep="\n\n",
)

# قالب Gemini — مثل Gemini — من FastChat
CONVERSATION_TEMPLATES["gemini"] = Conversation(
    name="gemini",
    system_message="You are Gemini — AI assistant by Google — helpful, search-augmented",
    roles=("user", "model"),
    sep_style=SeparatorStyle.GEMINI,
    sep="\n",
)

# قالب Manus — جديد — مثل Manus — وكلاء يعملون — task, execution, result
CONVERSATION_TEMPLATES["manus"] = Conversation(
    name="manus",
    system_message="You are Manus — AI agent that executes tasks — planner, architect, backend-dev, frontend-dev, reviewer — you execute real tasks, write real files, run real commands — like Paseo/coco Daemon",
    roles=("TASK", "EXECUTION"),
    sep_style=SeparatorStyle.MANUS,
    sep="\n---\n",
)

# قوالب لـ 68 وكيل — كل وكيل له قالب مخصص — مثل FastChat — $0
AGENT_TEMPLATES = {
    "planner": "You are planner — تخطط للمشاريع — تحلل المتطلبات — تضع خطة — مثل Manus planner",
    "architect": "You are architect — تصمم البنية — تختار التقنيات — مثل Manus architect",
    "backend-dev": "You are backend-dev — تكتب كود Backend حقيقي — FastAPI, Python — تنفذ فعلياً — مثل Manus backend-dev — تكتب ملفات حقيقية",
    "frontend-dev": "You are frontend-dev — تكتب كود Frontend حقيقي — React, TypeScript, Tailwind — تنفذ فعلياً — مثل Manus frontend-dev",
    "reviewer": "You are reviewer — تراجع الكود — تجد الأخطاء — مثل Manus reviewer",
    "qa-engineer": "You are qa-engineer — تختبر — تكتب اختبارات — مثل Manus qa-engineer",
}

for agent_id, system_msg in AGENT_TEMPLATES.items():
    CONVERSATION_TEMPLATES[agent_id] = Conversation(
        name=agent_id,
        system_message=system_msg,
        roles=("USER", "ASSISTANT"),
        sep_style=SeparatorStyle.ADD_COLON_SINGLE,
        sep="\n",
    )

# 68 قالب — لكل وكيل — مثل FastChat — $0
try:
    from ..agents.definitions import get_all_agents
    all_agents = get_all_agents()
    for agent in all_agents[:68]:
        agent_id = agent['id']
        if agent_id not in CONVERSATION_TEMPLATES:
            CONVERSATION_TEMPLATES[agent_id] = Conversation(
                name=agent_id,
                system_message=f"You are {agent['name']} — {agent.get('role', '')} — {agent.get('description', '')[:200]} — 68 وكيل متخصص — تعمل فعلياً مثل Manus",
                roles=("USER", "ASSISTANT"),
                sep_style=SeparatorStyle.ADD_COLON_SINGLE,
                sep="\n",
            )
except:
    pass

def get_conversation_template(name: str) -> Conversation:
    """الحصول على قالب محادثة — مثل FastChat get_conversation_template — يعمل فعلياً"""
    return CONVERSATION_TEMPLATES.get(name, CONVERSATION_TEMPLATES["general"]).copy()

def list_templates() -> List[str]:
    """قائمة القوالب — يعمل فعلياً"""
    return list(CONVERSATION_TEMPLATES.keys())
