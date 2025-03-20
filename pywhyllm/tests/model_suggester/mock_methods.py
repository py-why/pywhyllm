# def mock_add_behavior(self, other):
#     print("Mocking add behavior called")
#     return self
#
# def mock_iadd_behavior(self, other):
#     print("Mocking add behavior called")
#     return self
#
#
# def mock_getitem_behavior(self, key, value):
#     print("Mocking getitem behavior called")
#     if key == "description":
#         return value
#     else:
#         raise KeyError(f"Key '{key}' not found in LLM response")