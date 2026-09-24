import logging

# ruff: noqa
from odoo import models

from odoo.addons.base.models import ir_model

from ...... import upgrade_log
from .....odoo_patch import OdooPatch

_logger = logging.getLogger(__name__)


class IrModelConstraintPatch(OdooPatch):
    target = ir_model.IrModelConstraint
    method_names = ["_reflect_table_object"]

    def _reflect_table_object(self, model):
        """Reflect the _table_objects of the given model."""
        data_list = IrModelConstraintPatch._reflect_table_object._original_method(
            self, model
        )
        # Begin OpenUpgrade addition
        for conname, cons in model._table_objects.items():
            if conname and cons._module:
                upgrade_log.log_xml_id(
                    self.env.cr, cons._module, f"{cons._module}.constraint_{conname}"
                )
        # End OpenUpgrade addition
        return data_list
