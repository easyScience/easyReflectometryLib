__author__ = 'github.com/arm61'
__version__ = '0.0.1'
"""
Tests for Refnx class module
"""

import os
import unittest
import numpy as np
from numpy.testing import assert_almost_equal, assert_equal
from easyReflectometryLib.Calculators.refnx import Refnx


class TestRefnx(unittest.TestCase):
    def test_init(self):
        p = Refnx()
        assert_equal(list(p.storage.keys()), ['material', 'layer', 'item'])

    def test_create_material(self):
        p = Refnx()
        p.create_material('Si')
        assert_equal(list(p.storage['material'].keys()), ['Si'])
        assert_almost_equal(p.storage['material']['Si'].real.value, 0.0)
        assert_almost_equal(p.storage['material']['Si'].imag.value, 0.0)

    def test_update_material(self):
        p = Refnx()
        p.create_material('B')
        p.update_material('B', real=6.908, imag=-0.278)
        assert_equal(list(p.storage['material'].keys()), ['B'])
        assert_almost_equal(p.storage['material']['B'].real.value, 6.908)
        assert_almost_equal(p.storage['material']['B'].imag.value, -0.278)

    def test_get_material_value(self):
        p = Refnx()
        p.create_material('B')
        p.update_material('B', real=6.908, imag=-0.278)
        assert_equal(list(p.storage['material'].keys()), ['B'])
        assert_almost_equal(p.get_material_value('B', 'real'), 6.908)
        assert_almost_equal(p.get_material_value('B', 'imag'), -0.278)

    def test_create_layer(self):
        p = Refnx()
        p.create_material('Si')
        p.create_layer('Si_layer', 'Si')
        p.update_material('Si', real=6.908, imag=-0.278)
        assert_equal(list(p.storage['layer'].keys()), ['Si_layer'])
        assert_equal(p.storage['layer']['Si_layer'].sld.real.value, 6.908)
        assert_almost_equal(p.storage['layer']['Si_layer'].thick.value, 0.0)
        assert_almost_equal(p.storage['layer']['Si_layer'].rough.value, 0.0)

    def test_update_layer(self):
        p = Refnx()
        p.create_material('Si')
        p.create_layer('Si_layer', 'Si')
        p.update_layer('Si_layer', thick=10.0, rough=1.2)
        assert_equal(list(p.storage['layer'].keys()), ['Si_layer'])
        assert_almost_equal(p.storage['layer']['Si_layer'].thick.value, 10.0)
        assert_almost_equal(p.storage['layer']['Si_layer'].rough.value, 1.2)

    def test_get_layer_value(self):
        p = Refnx()
        p.create_material('Si')
        p.create_layer('Si_layer', 'Si')
        p.update_layer('Si_layer', thick=10.0, rough=1.2)
        assert_equal(list(p.storage['layer'].keys()), ['Si_layer'])
        assert_almost_equal(p.get_layer_value('Si_layer', 'thick'), 10.0)
        assert_almost_equal(p.get_layer_value('Si_layer', 'rough'), 1.2)

    def test_create_item(self):
        p = Refnx()
        p.create_material('Si')
        p.create_layer('Si_layer', 'Si')
        p.create_item('ML')
        assert_equal(list(p.storage['item'].keys()), ['ML'])
        assert_equal(p.storage['item']['ML'].components, [])
        assert_equal(p.storage['item']['ML'].repeats.value, 1.0)

    def test_add_layer1(self):
        p = Refnx()
        p.create_material('Si')
        p.create_layer('Si_layer', 'Si')
        p.update_layer('Si_layer', thick=10.0, rough=1.2)
        p.create_item('ML')
        p.add_layer('ML', 'Si_layer')
        assert_equal(len(p.storage['item']['ML'].components), 1)
        assert_equal(p.storage['item']['ML'].components[0].thick.value, 10.0)
        assert_equal(p.storage['item']['ML'].components[0].rough.value, 1.2)

    def test_add_layer2(self):
        p = Refnx()
        p.create_material('Si')
        p.create_material('B')
        p.update_material('B', real=6.908, imag=-0.278)
        p.create_layer('Si_layer', 'Si')
        p.create_layer('B_layer', 'B')
        p.update_layer('Si_layer', thick=10.0, rough=1.2)
        p.update_layer('B_layer', thick=5.0, rough=0.0)
        p.create_item('ML')
        p.add_layer('ML', 'Si_layer')
        p.add_layer('ML', 'B_layer')
        assert_equal(len(p.storage['item']['ML'].components), 2)
        assert_equal(p.storage['item']['ML'].components[0].thick.value, 10.0)
        assert_equal(p.storage['item']['ML'].components[0].rough.value, 1.2)
        assert_equal(p.storage['item']['ML'].components[1].thick.value, 5.0)
        assert_equal(p.storage['item']['ML'].components[1].rough.value, 0.0)

    def test_remove_layer(self):
        p = Refnx()
        p.create_material('Si')
        p.create_material('B')
        p.update_material('B', real=6.908, imag=-0.278)
        p.create_layer('Si_layer', 'Si')
        p.create_layer('B_layer', 'B')
        p.update_layer('Si_layer', thick=10.0, rough=1.2)
        p.update_layer('B_layer', thick=5.0, rough=0.0)
        p.create_item('ML')
        p.add_layer('ML', 'Si_layer')
        p.add_layer('ML', 'B_layer')
        p.remove_layer('ML', 'Si_layer')
        assert_equal(len(p.storage['item']['ML'].components), 1)
        assert_equal(p.storage['item']['ML'].components[0].thick.value, 5.0)
        assert_equal(p.storage['item']['ML'].components[0].rough.value, 0.0)

    def test_move_layer_up(self):
        p = Refnx()
        p.create_material('Si')
        p.create_material('B')
        p.update_material('B', real=6.908, imag=-0.278)
        p.create_layer('Si_layer', 'Si')
        p.create_layer('B_layer', 'B')
        p.update_layer('Si_layer', thick=10.0, rough=1.2)
        p.update_layer('B_layer', thick=5.0, rough=0.0)
        p.create_item('ML')
        p.add_layer('ML', 'Si_layer')
        p.add_layer('ML', 'B_layer')
        assert_equal(len(p.storage['item']['ML'].components), 2)
        assert_equal(p.storage['item']['ML'].components[0].thick.value, 10.0)
        assert_equal(p.storage['item']['ML'].components[0].rough.value, 1.2)
        assert_equal(p.storage['item']['ML'].components[1].thick.value, 5.0)
        assert_equal(p.storage['item']['ML'].components[1].rough.value, 0.0)
        p.move_layer_up('ML', 'B_layer')
        assert_equal(len(p.storage['item']['ML'].components), 2)
        assert_equal(p.storage['item']['ML'].components[1].thick.value, 10.0)
        assert_equal(p.storage['item']['ML'].components[1].rough.value, 1.2)
        assert_equal(p.storage['item']['ML'].components[0].thick.value, 5.0)
        assert_equal(p.storage['item']['ML'].components[0].rough.value, 0.0)

    def test_move_layer_down(self):
        p = Refnx()
        p.create_material('Si')
        p.create_material('B')
        p.update_material('B', real=6.908, imag=-0.278)
        p.create_layer('Si_layer', 'Si')
        p.create_layer('B_layer', 'B')
        p.update_layer('Si_layer', thick=10.0, rough=1.2)
        p.update_layer('B_layer', thick=5.0, rough=0.0)
        p.create_item('ML')
        p.add_layer('ML', 'Si_layer')
        p.add_layer('ML', 'B_layer')
        assert_equal(len(p.storage['item']['ML'].components), 2)
        assert_equal(p.storage['item']['ML'].components[0].thick.value, 10.0)
        assert_equal(p.storage['item']['ML'].components[0].rough.value, 1.2)
        assert_equal(p.storage['item']['ML'].components[1].thick.value, 5.0)
        assert_equal(p.storage['item']['ML'].components[1].rough.value, 0.0)
        p.move_layer_down('ML', 'Si_layer')
        assert_equal(len(p.storage['item']['ML'].components), 2)
        assert_equal(p.storage['item']['ML'].components[1].thick.value, 10.0)
        assert_equal(p.storage['item']['ML'].components[1].rough.value, 1.2)
        assert_equal(p.storage['item']['ML'].components[0].thick.value, 5.0)
        assert_equal(p.storage['item']['ML'].components[0].rough.value, 0.0)

    def test_update_reps(self):
        p = Refnx()
        p.create_material('Si')
        p.create_material('B')
        p.update_material('B', real=6.908, imag=-0.278)
        p.create_layer('Si_layer', 'Si')
        p.create_layer('B_layer', 'B')
        p.update_layer('Si_layer', thick=10.0, rough=1.2)
        p.update_layer('B_layer', thick=5.0, rough=0.0)
        p.create_item('ML')
        p.add_layer('ML', 'Si_layer')
        p.add_layer('ML', 'B_layer')
        assert_almost_equal(p.storage['item']['ML'].repeats.value, 1.0)
        p.update_reps('ML', 3)
        assert_almost_equal(p.storage['item']['ML'].repeats.value, 3.0)

    def test_get_reps(self):
        p = Refnx()
        p.create_material('Si')
        p.create_material('B')
        p.update_material('B', real=6.908, imag=-0.278)
        p.create_layer('Si_layer', 'Si')
        p.create_layer('B_layer', 'B')
        p.update_layer('Si_layer', thick=10.0, rough=1.2)
        p.update_layer('B_layer', thick=5.0, rough=0.0)
        p.create_item('ML')
        p.add_layer('ML', 'Si_layer')
        p.add_layer('ML', 'B_layer')
        assert_almost_equal(p.get_reps('ML'), 1.0)
        p.update_reps('ML', 3)
        assert_almost_equal(p.get_reps('ML'), 3.0)

    def test_create_model(self):
        p = Refnx()
        p.create_model()
        assert_equal(p.storage['model'].structure.components, [])
        assert_almost_equal(p.storage['model'].scale.value, 1)
        assert_almost_equal(p.storage['model'].bkg.value, 0)
        assert_almost_equal(p.storage['model'].dq.value, 5.0)

    def test_add_item_layer(self):
        p = Refnx()
        p.create_material('B')
        p.update_material('B', real=6.908, imag=-0.278)
        p.create_layer('B_layer', 'B')
        p.update_layer('B_layer', thick=10.0, rough=1.2)
        p.create_model()
        p.add_item('B_layer')
        assert_equal(len(p.storage['model'].structure.components), 1)
        assert_equal(p.storage['model'].structure.components[0].thick.value,
                     10.0)
        assert_equal(p.storage['model'].structure.components[0].rough.value,
                     1.2)
        assert_equal(p.storage['model'].structure.components[0].sld.real.value,
                     6.908)
        assert_equal(p.storage['model'].structure.components[0].sld.imag.value,
                     -0.278)

    def test_add_item_layer2(self):
        p = Refnx()
        p.create_material('B')
        p.update_material('B', real=6.908, imag=-0.278)
        p.create_material('B2')
        p.update_material('B2', real=16.908, imag=-10.278)
        p.create_layer('B_layer', 'B')
        p.update_layer('B_layer', thick=10.0, rough=1.2)
        p.create_layer('B2_layer', 'B2')
        p.update_layer('B2_layer', thick=1.0, rough=0.2)
        p.create_model()
        p.add_item('B_layer')
        p.add_item('B2_layer')
        assert_equal(len(p.storage['model'].structure.components), 2)
        assert_equal(p.storage['model'].structure.components[0].thick.value,
                     10.0)
        assert_equal(p.storage['model'].structure.components[0].rough.value,
                     1.2)
        assert_equal(p.storage['model'].structure.components[0].sld.real.value,
                     6.908)
        assert_equal(p.storage['model'].structure.components[0].sld.imag.value,
                     -0.278)
        assert_equal(p.storage['model'].structure.components[1].thick.value,
                     1.0)
        assert_equal(p.storage['model'].structure.components[1].rough.value,
                     0.2)
        assert_equal(p.storage['model'].structure.components[1].sld.real.value,
                     16.908)
        assert_equal(p.storage['model'].structure.components[1].sld.imag.value,
                     -10.278)

    def test_add_item_item1(self):
        p = Refnx()
        p.create_material('B')
        p.update_material('B', real=6.908, imag=-0.278)
        p.create_material('B2')
        p.update_material('B2', real=16.908, imag=-10.278)
        p.create_layer('B_layer', 'B')
        p.update_layer('B_layer', thick=10.0, rough=1.2)
        p.create_layer('B2_layer', 'B2')
        p.update_layer('B2_layer', thick=1.0, rough=0.2)
        p.create_item('ML')
        p.add_layer('ML', 'B_layer')
        p.add_layer('ML', 'B2_layer')
        p.create_model()
        p.add_item('ML')
        assert_equal(len(p.storage['model'].structure.components), 1)
        assert_equal(
            len(p.storage['model'].structure.components[0].components), 2)
        assert_equal(p.storage['model'].structure.components[0].repeats.value,
                     1)
        assert_equal(
            p.storage['model'].structure.components[0].components[0].thick.
            value, 10.0)
        assert_equal(
            p.storage['model'].structure.components[0].components[0].rough.
            value, 1.2)
        assert_equal(
            p.storage['model'].structure.components[0].components[0].sld.real.
            value, 6.908)
        assert_equal(
            p.storage['model'].structure.components[0].components[0].sld.imag.
            value, -0.278)
        assert_equal(
            p.storage['model'].structure.components[0].components[1].thick.
            value, 1.0)
        assert_equal(
            p.storage['model'].structure.components[0].components[1].rough.
            value, 0.2)
        assert_equal(
            p.storage['model'].structure.components[0].components[1].sld.real.
            value, 16.908)
        assert_equal(
            p.storage['model'].structure.components[0].components[1].sld.imag.
            value, -10.278)

    def test_add_item_item2(self):
        p = Refnx()
        p.create_material('B')
        p.update_material('B', real=6.908, imag=-0.278)
        p.create_material('B2')
        p.update_material('B2', real=16.908, imag=-10.278)
        p.create_layer('B_layer', 'B')
        p.update_layer('B_layer', thick=10.0, rough=1.2)
        p.create_layer('B2_layer', 'B2')
        p.update_layer('B2_layer', thick=1.0, rough=0.2)
        p.create_item('ML')
        p.create_item('ML2')
        p.add_layer('ML', 'B_layer')
        p.add_layer('ML', 'B2_layer')
        p.add_layer('ML2', 'B2_layer')
        p.add_layer('ML2', 'B_layer')
        p.create_model()
        p.add_item('ML')
        p.add_item('ML2')
        assert_equal(len(p.storage['model'].structure.components), 2)
        assert_equal(
            len(p.storage['model'].structure.components[0].components), 2)
        assert_equal(p.storage['model'].structure.components[1].repeats.value,
                     1)
        assert_equal(
            p.storage['model'].structure.components[1].components[0].thick.
            value, 1.0)
        assert_equal(
            p.storage['model'].structure.components[1].components[0].rough.
            value, 0.2)
        assert_equal(
            p.storage['model'].structure.components[1].components[0].sld.real.
            value, 16.908)
        assert_equal(
            p.storage['model'].structure.components[1].components[0].sld.imag.
            value, -10.278)

    def test_remove_item_layer(self):
        p = Refnx()
        p.create_material('B')
        p.update_material('B', real=6.908, imag=-0.278)
        p.create_material('B2')
        p.update_material('B2', real=16.908, imag=-10.278)
        p.create_layer('B_layer', 'B')
        p.update_layer('B_layer', thick=10.0, rough=1.2)
        p.create_layer('B2_layer', 'B2')
        p.update_layer('B2_layer', thick=1.0, rough=0.2)
        p.create_model()
        p.add_item('B_layer')
        p.add_item('B2_layer')
        assert_equal(len(p.storage['model'].structure.components), 2)
        assert_equal(p.storage['model'].structure.components[0].thick.value,
                     10.0)
        assert_equal(p.storage['model'].structure.components[0].rough.value,
                     1.2)
        assert_equal(p.storage['model'].structure.components[0].sld.real.value,
                     6.908)
        assert_equal(p.storage['model'].structure.components[0].sld.imag.value,
                     -0.278)
        assert_equal(p.storage['model'].structure.components[1].thick.value,
                     1.0)
        assert_equal(p.storage['model'].structure.components[1].rough.value,
                     0.2)
        assert_equal(p.storage['model'].structure.components[1].sld.real.value,
                     16.908)
        assert_equal(p.storage['model'].structure.components[1].sld.imag.value,
                     -10.278)
        p.remove_item('B2_layer')
        assert_equal(len(p.storage['model'].structure.components), 1)
        assert_equal(p.storage['model'].structure.components[0].thick.value,
                     10.0)
        assert_equal(p.storage['model'].structure.components[0].rough.value,
                     1.2)
        assert_equal(p.storage['model'].structure.components[0].sld.real.value,
                     6.908)
        assert_equal(p.storage['model'].structure.components[0].sld.imag.value,
                     -0.278)

    def test_remove_item_item(self):
        p = Refnx()
        p.create_material('B')
        p.update_material('B', real=6.908, imag=-0.278)
        p.create_material('B2')
        p.update_material('B2', real=16.908, imag=-10.278)
        p.create_layer('B_layer', 'B')
        p.update_layer('B_layer', thick=10.0, rough=1.2)
        p.create_layer('B2_layer', 'B2')
        p.update_layer('B2_layer', thick=1.0, rough=0.2)
        p.create_item('ML')
        p.create_item('ML2')
        p.add_layer('ML', 'B_layer')
        p.add_layer('ML', 'B2_layer')
        p.add_layer('ML2', 'B2_layer')
        p.add_layer('ML2', 'B_layer')
        p.create_model()
        p.add_item('ML')
        p.add_item('ML2')
        assert_equal(len(p.storage['model'].structure.components), 2)
        assert_equal(
            len(p.storage['model'].structure.components[0].components), 2)
        assert_equal(p.storage['model'].structure.components[1].repeats.value,
                     1)
        assert_equal(
            p.storage['model'].structure.components[1].components[0].thick.
            value, 1.0)
        assert_equal(
            p.storage['model'].structure.components[1].components[0].rough.
            value, 0.2)
        assert_equal(
            p.storage['model'].structure.components[1].components[0].sld.real.
            value, 16.908)
        assert_equal(
            p.storage['model'].structure.components[1].components[0].sld.imag.
            value, -10.278)
        p.remove_item('ML2')
        assert_equal(len(p.storage['model'].structure.components), 1)

    def test_move_item_up(self):
        p = Refnx()
        p.create_material('B')
        p.update_material('B', real=6.908, imag=-0.278)
        p.create_material('B2')
        p.update_material('B2', real=16.908, imag=-10.278)
        p.create_layer('B_layer', 'B')
        p.update_layer('B_layer', thick=10.0, rough=1.2)
        p.create_layer('B2_layer', 'B2')
        p.update_layer('B2_layer', thick=1.0, rough=0.2)
        p.create_item('ML')
        p.create_item('ML2')
        p.add_layer('ML', 'B_layer')
        p.add_layer('ML', 'B2_layer')
        p.add_layer('ML2', 'B2_layer')
        p.add_layer('ML2', 'B_layer')
        p.create_model()
        p.add_item('ML')
        p.add_item('ML2')
        assert_equal(len(p.storage['model'].structure.components), 2)
        assert_equal(
            len(p.storage['model'].structure.components[0].components), 2)
        assert_equal(p.storage['model'].structure.components[1].repeats.value,
                     1)
        assert_equal(
            p.storage['model'].structure.components[1].components[0].thick.
            value, 1.0)
        assert_equal(
            p.storage['model'].structure.components[1].components[0].rough.
            value, 0.2)
        assert_equal(
            p.storage['model'].structure.components[1].components[0].sld.real.
            value, 16.908)
        assert_equal(
            p.storage['model'].structure.components[1].components[0].sld.imag.
            value, -10.278)
        p.move_item_up('ML2')
        assert_equal(p.storage['model'].structure.components[1].repeats.value,
                     1)
        assert_equal(
            p.storage['model'].structure.components[0].components[0].thick.
            value, 1.0)
        assert_equal(
            p.storage['model'].structure.components[0].components[0].rough.
            value, 0.2)
        assert_equal(
            p.storage['model'].structure.components[0].components[0].sld.real.
            value, 16.908)
        assert_equal(
            p.storage['model'].structure.components[0].components[0].sld.imag.
            value, -10.278)

    def test_move_item_down(self):
        p = Refnx()
        p.create_material('B')
        p.update_material('B', real=6.908, imag=-0.278)
        p.create_material('B2')
        p.update_material('B2', real=16.908, imag=-10.278)
        p.create_layer('B_layer', 'B')
        p.update_layer('B_layer', thick=10.0, rough=1.2)
        p.create_layer('B2_layer', 'B2')
        p.update_layer('B2_layer', thick=1.0, rough=0.2)
        p.create_item('ML')
        p.create_item('ML2')
        p.add_layer('ML', 'B_layer')
        p.add_layer('ML', 'B2_layer')
        p.add_layer('ML2', 'B2_layer')
        p.add_layer('ML2', 'B_layer')
        p.create_model()
        p.add_item('ML')
        p.add_item('ML2')
        assert_equal(len(p.storage['model'].structure.components), 2)
        assert_equal(
            len(p.storage['model'].structure.components[0].components), 2)
        assert_equal(p.storage['model'].structure.components[1].repeats.value,
                     1)
        assert_equal(
            p.storage['model'].structure.components[0].components[0].thick.
            value, 10.0)
        assert_equal(
            p.storage['model'].structure.components[0].components[0].rough.
            value, 1.2)
        assert_equal(
            p.storage['model'].structure.components[0].components[0].sld.real.
            value, 6.908)
        assert_equal(
            p.storage['model'].structure.components[0].components[0].sld.imag.
            value, -0.278)
        p.move_item_down('ML')
        assert_equal(p.storage['model'].structure.components[0].repeats.value,
                     1)
        assert_equal(
            p.storage['model'].structure.components[1].components[0].thick.
            value, 10.0)
        assert_equal(
            p.storage['model'].structure.components[1].components[0].rough.
            value, 1.2)
        assert_equal(
            p.storage['model'].structure.components[1].components[0].sld.real.
            value, 6.908)
        assert_equal(
            p.storage['model'].structure.components[1].components[0].sld.imag.
            value, -0.278)

    def test_update_model(self):
        p = Refnx()
        p.create_material('B')
        p.update_material('B', real=6.908, imag=-0.278)
        p.create_material('B2')
        p.update_material('B2', real=16.908, imag=-10.278)
        p.create_layer('B_layer', 'B')
        p.update_layer('B_layer', thick=10.0, rough=1.2)
        p.create_layer('B2_layer', 'B2')
        p.update_layer('B2_layer', thick=1.0, rough=0.2)
        p.create_item('ML')
        p.add_layer('ML', 'B_layer')
        p.add_layer('ML', 'B2_layer')
        p.create_model()
        p.add_item('ML')
        p.update_model(scale=2, bkg=1e-3, dq=2.0)
        assert_almost_equal(p.storage['model'].scale.value, 2)
        assert_almost_equal(p.storage['model'].bkg.value, 1e-3)
        assert_almost_equal(p.storage['model'].dq.value, 2.0)

    def test_get_model_value(self):
        p = Refnx()
        p.create_material('B')
        p.update_material('B', real=6.908, imag=-0.278)
        p.create_material('B2')
        p.update_material('B2', real=16.908, imag=-10.278)
        p.create_layer('B_layer', 'B')
        p.update_layer('B_layer', thick=10.0, rough=1.2)
        p.create_layer('B2_layer', 'B2')
        p.update_layer('B2_layer', thick=1.0, rough=0.2)
        p.create_item('ML')
        p.add_layer('ML', 'B_layer')
        p.add_layer('ML', 'B2_layer')
        p.create_model()
        p.add_item('ML')
        p.update_model(scale=2, bkg=1e-3, dq=2.0)
        assert_almost_equal(p.get_model_value('scale'), 2)
        assert_almost_equal(p.get_model_value('bkg'), 1e-3)
        assert_almost_equal(p.get_model_value('dq'), 2.0)

    def test_calculate(self):
        p = Refnx()
        p.create_material('Material1')
        p.update_material('Material1', real=0.000, imag=0.000)
        p.create_material('Material2')
        p.update_material('Material2', real=2.000, imag=0.000)
        p.create_material('Material3')
        p.update_material('Material3', real=4.000, imag=0.000)
        p.create_layer('Layer1', 'Material1')
        p.update_layer('Layer1', thick=0.0, rough=0.0)
        p.create_layer('Layer2', 'Material2')
        p.update_layer('Layer2', thick=10.0, rough=1.0)
        p.create_layer('Layer3', 'Material3')
        p.update_layer('Layer3', thick=0.0, rough=1.0)
        p.create_model()
        p.add_item('Layer1')
        p.add_item('Layer2')
        p.add_item('Layer3')
        q = np.linspace(0.001, 0.3, 10)
        expected = [
            9.99956517e-01, 2.16286891e-03, 1.14086254e-04, 1.93031759e-05,
            4.94188894e-06, 1.54191953e-06, 5.45592112e-07, 2.26619392e-07,
            1.26726993e-07, 1.01842852e-07
        ]
        assert_almost_equal(p.calculate(q), expected)
