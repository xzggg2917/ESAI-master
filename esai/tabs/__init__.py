"""
Tab Modules for ESAI
====================

This package contains the tab implementations for the ESAI application.
Each tab corresponds to a scoring dimension.

Tabs:
- weight_tab: Weight configuration tab (Set)
- sc_tab: Sample Collection tab
- sp_tab: Sample Preparation tab
- at_tab: Analytical Technique tab
- economy_tab: Economy tab
- method_tab: Method tab
- operator_tab: Operator Safety tab
- reagent_tab: Reagent tab
- waste_tab: Waste tab
"""

from esai.tabs.base_tab import BaseTab, QuestionConfig, RadioChoice
from esai.tabs.weight_tab import WeightTab
from esai.tabs.sc_tab import SCTab
from esai.tabs.sp_tab import SPTab
from esai.tabs.at_tab import ATTab
from esai.tabs.economy_tab import EconomyTab
from esai.tabs.method_tab import MethodTab
from esai.tabs.operator_tab import OperatorTab
from esai.tabs.reagent_tab import ReagentTab
from esai.tabs.waste_tab import WasteTab

__all__ = [
    'BaseTab',
    'QuestionConfig',
    'RadioChoice',
    'WeightTab',
    'SCTab',
    'SPTab',
    'ATTab',
    'EconomyTab',
    'MethodTab',
    'OperatorTab',
    'ReagentTab',
    'WasteTab',
]
