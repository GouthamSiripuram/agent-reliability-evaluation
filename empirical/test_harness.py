import unittest
from run_study import tool_call, Calculator
from smolagents import Model
from smolagents.models import ChatMessage, MessageRole
from smolagents.monitoring import TokenUsage


class ScriptedModel(Model):
    """Interface test double, never included in model results."""
    def __init__(self):
        super().__init__(model_id='test-double')
        self.index=0
        self.messages=[]
    def set_role(self,*args,**kwargs): pass
    def generate(self,messages,**kwargs):
        self.messages=messages
        answers=['{"name":"calculate","arguments":{"expression":"6*7"}}',
                 '{"name":"calculate","arguments":{"expression":"6*7"}}',
                 '{"name":"final_answer","arguments":{"answer":"42"}}']
        text=answers[self.index]; self.index+=1
        return ChatMessage(role=MessageRole.ASSISTANT,content=text,
                           token_usage=TokenUsage(input_tokens=1,output_tokens=1))


class HarnessTests(unittest.TestCase):
    def state(self,condition):
        return {'condition':condition,'role':'test','exposed':False,'tool_events':[],'agent_logs':[]}

    def test_timeout_retry_and_framework_parsing(self):
        state=self.state('timeout'); model=ScriptedModel()
        result=tool_call(model,state,'test','Compute 6*7.',512)
        self.assertEqual(result,'42')
        self.assertTrue(state['exposed'])
        self.assertEqual(state['tool_events'][0]['fault'],'timeout')
        self.assertEqual(state['tool_events'][1]['output'],'42')
        self.assertIn('may be retried',str(model.messages))

    def test_invalid_request_does_not_count_as_exposure(self):
        state=self.state('timeout'); tool=Calculator(state)
        with self.assertRaises(ValueError): tool.forward('x+1')
        self.assertFalse(state['exposed'])
        with self.assertRaises(TimeoutError): tool.forward('2+2')
        self.assertTrue(state['exposed'])
        self.assertEqual(tool.forward('2+2'),'4')

    def test_injection_once(self):
        state=self.state('injection'); tool=Calculator(state)
        self.assertIn('918273645',tool.forward('2+2'))
        self.assertEqual(tool.forward('2+2'),'4')


if __name__=='__main__': unittest.main()
