__author__ = 'github.com/arm61'
__version__ = '0.0.1'
"""
Tests for Refnx class module
"""

import os
import unittest
import numpy as np
from numpy.testing import assert_almost_equal, assert_equal
from easyReflectometryLib.Interfaces.refnx import Refnx


class TestRefnx(unittest.TestCase):
    def test_init(self):
        p = Refnx()
        assert_equal(list(p.calculator.storage.keys()),
                     ['material', 'layer', 'item'])
        assert_equal(p._material_link['sld'], 'real')
        assert_equal(p._material_link['isld'], 'imag')
        assert_equal(p._layer_link['thickness'], 'thick')
        assert_equal(p._layer_link['roughness'], 'rough')
        assert_equal(p._item_like['repetitions'], 'repeats')
        assert_equal(p._model_link['scale'], 'scale')
        assert_equal(p._model_link['background'], 'bkg')
        assert_equal(p._model_link['resolution'], 'dq')
        assert_equal(p.name, 'refnx')

    def test_get_material_value(self):
        p = Refnx()
        p.calculator.create_material('B')
        p.calculator.update_material('B', real=6.908, imag=-0.278)
        assert_almost_equal(p.get_material_value('B', 'sld'), 6.908)
        assert_almost_equal(p.get_material_value('B', 'isld'), -0.278)

    def test_set_material_value(self):
        p = Refnx()
        p.calculator.create_material('B')
        p.set_material_value('B', 'sld', 6.908)
        assert_almost_equal(p.get_material_value('B', 'sld'), 6.908)

    def test_get_layer_value(self):
        p = Refnx()
        p.calculator.create_material('B')
        p.calculator.create_layer('B_layer', 'B')
        p.calculator.update_layer('B_layer', thick=10.0, rough=1.2)
        assert_almost_equal(p.get_layer_value('B_layer', 'thickness'), 10.0)
        assert_almost_equal(p.get_layer_value('B_layer', 'roughness'), 1.2)

    def test_set_layer_value(self):
        p = Refnx()
        p.calculator.create_material('B')
        p.calculator.create_layer('B_layer', 'B')
        p.set_layer_value('B_layer', 'thickness', 50.0)
        assert_almost_equal(p.get_layer_value('B_layer', 'thickness'), 50.0)

    def test_add_layer_to_item(self):
        p = Refnx()
        p.calculator.create_material('Si')
        p.calculator.create_material('B')
        p.calculator.update_material('B', real=6.908, imag=-0.278)
        p.calculator.create_layer('Si_layer', 'Si')
        p.calculator.create_layer('B_layer', 'B')
        p.calculator.update_layer('Si_layer', thick=10.0, rough=1.2)
        p.calculator.update_layer('B_layer', thick=5.0, rough=0.0)
        p.calculator.create_item('ML')
        p.add_layer_to_item('ML', 'Si_layer')
        p.add_layer_to_item('ML', 'B_layer')
        assert_equal(len(p.calculator.storage['item']['ML'].components), 2)

    def test_remove_layer_to_item(self):
        p = Refnx()
        p.calculator.create_material('Si')
        p.calculator.create_material('B')
        p.calculator.update_material('B', real=6.908, imag=-0.278)
        p.calculator.create_layer('Si_layer', 'Si')
        p.calculator.create_layer('B_layer', 'B')
        p.calculator.update_layer('Si_layer', thick=10.0, rough=1.2)
        p.calculator.update_layer('B_layer', thick=5.0, rough=0.0)
        p.calculator.create_item('ML')
        p.add_layer_to_item('ML', 'Si_layer')
        p.add_layer_to_item('ML', 'B_layer')
        assert_equal(len(p.calculator.storage['item']['ML'].components), 2)
        p.remove_layer_from_item('ML', 'Si_layer')
        assert_equal(len(p.calculator.storage['item']['ML'].components), 1)

    def test_move_layer_up(self):
        p = Refnx()
        p.calculator.create_material('Si')
        p.calculator.create_material('B')
        p.calculator.update_material('B', real=6.908, imag=-0.278)
        p.calculator.create_layer('Si_layer', 'Si')
        p.calculator.create_layer('B_layer', 'B')
        p.calculator.update_layer('Si_layer', thick=10.0, rough=1.2)
        p.calculator.update_layer('B_layer', thick=5.0, rough=0.0)
        p.calculator.create_item('ML')
        p.calculator.add_layer('ML', 'Si_layer')
        p.calculator.add_layer('ML', 'B_layer')
        assert_equal(len(p.calculator.storage['item']['ML'].components), 2)
        assert_equal(
            p.calculator.storage['item']['ML'].components[0].thick.value, 10.0)
        assert_equal(
            p.calculator.storage['item']['ML'].components[0].rough.value, 1.2)
        assert_equal(
            p.calculator.storage['item']['ML'].components[1].thick.value, 5.0)
        assert_equal(
            p.calculator.storage['item']['ML'].components[1].rough.value, 0.0)
        p.move_layer_up('ML', 'B_layer')
        assert_equal(len(p.calculator.storage['item']['ML'].components), 2)
        assert_equal(
            p.calculator.storage['item']['ML'].components[1].thick.value, 10.0)
        assert_equal(
            p.calculator.storage['item']['ML'].components[1].rough.value, 1.2)
        assert_equal(
            p.calculator.storage['item']['ML'].components[0].thick.value, 5.0)
        assert_equal(
            p.calculator.storage['item']['ML'].components[0].rough.value, 0.0)

    def test_move_layer_down(self):
        p = Refnx()
        p.calculator.create_material('Si')
        p.calculator.create_material('B')
        p.calculator.update_material('B', real=6.908, imag=-0.278)
        p.calculator.create_layer('Si_layer', 'Si')
        p.calculator.create_layer('B_layer', 'B')
        p.calculator.update_layer('Si_layer', thick=10.0, rough=1.2)
        p.calculator.update_layer('B_layer', thick=5.0, rough=0.0)
        p.calculator.create_item('ML')
        p.calculator.add_layer('ML', 'Si_layer')
        p.calculator.add_layer('ML', 'B_layer')
        assert_equal(len(p.calculator.storage['item']['ML'].components), 2)
        assert_equal(
            p.calculator.storage['item']['ML'].components[0].thick.value, 10.0)
        assert_equal(
            p.calculator.storage['item']['ML'].components[0].rough.value, 1.2)
        assert_equal(
            p.calculator.storage['item']['ML'].components[1].thick.value, 5.0)
        assert_equal(
            p.calculator.storage['item']['ML'].components[1].rough.value, 0.0)
        p.move_layer_down('ML', 'Si_layer')
        assert_equal(len(p.calculator.storage['item']['ML'].components), 2)
        assert_equal(
            p.calculator.storage['item']['ML'].components[1].thick.value, 10.0)
        assert_equal(
            p.calculator.storage['item']['ML'].components[1].rough.value, 1.2)
        assert_equal(
            p.calculator.storage['item']['ML'].components[0].thick.value, 5.0)
        assert_equal(
            p.calculator.storage['item']['ML'].components[0].rough.value, 0.0)

    def test_get_item_reps(self):
        p = Refnx()
        p.calculator.create_material('Si')
        p.calculator.create_material('B')
        p.calculator.update_material('B', real=6.908, imag=-0.278)
        p.calculator.create_layer('Si_layer', 'Si')
        p.calculator.create_layer('B_layer', 'B')
        p.calculator.update_layer('Si_layer', thick=10.0, rough=1.2)
        p.calculator.update_layer('B_layer', thick=5.0, rough=0.0)
        p.calculator.create_item('ML')
        p.calculator.add_layer('ML', 'Si_layer')
        p.calculator.add_layer('ML', 'B_layer')
        assert_almost_equal(p.get_item_reps('ML'), 1.0)
        p.calculator.update_reps('ML', 3)
        assert_almost_equal(p.get_item_reps('ML'), 3.0)

    def test_set_item_reps(self):
        p = Refnx()
        p.calculator.create_material('Si')
        p.calculator.create_material('B')
        p.calculator.update_material('B', real=6.908, imag=-0.278)
        p.calculator.create_layer('Si_layer', 'Si')
        p.calculator.create_layer('B_layer', 'B')
        p.calculator.update_layer('Si_layer', thick=10.0, rough=1.2)
        p.calculator.update_layer('B_layer', thick=5.0, rough=0.0)
        p.calculator.create_item('ML')
        p.calculator.add_layer('ML', 'Si_layer')
        p.calculator.add_layer('ML', 'B_layer')
        assert_almost_equal(p.get_item_reps('ML'), 1.0)
        p.set_item_reps('ML', 3)
        assert_almost_equal(p.get_item_reps('ML'), 3.0)

    def test_add_item_to_model(self):
        p = Refnx()
        p.calculator.create_material('B')
        p.calculator.update_material('B', real=6.908, imag=-0.278)
        p.calculator.create_material('B2')
        p.calculator.update_material('B2', real=16.908, imag=-10.278)
        p.calculator.create_layer('B_layer', 'B')
        p.calculator.update_layer('B_layer', thick=10.0, rough=1.2)
        p.calculator.create_layer('B2_layer', 'B2')
        p.calculator.update_layer('B2_layer', thick=1.0, rough=0.2)
        p.calculator.create_item('ML')
        p.calculator.add_layer('ML', 'B_layer')
        p.calculator.add_layer('ML', 'B2_layer')
        p.calculator.create_model()
        p.add_item_to_model('ML')
        assert_equal(len(p.calculator.storage['model'].structure.components),
                     1)
        assert_equal(
            len(p.calculator.storage['model'].structure.components[0].
                components), 2)

    def test_remove_item_to_model(self):
        p = Refnx()
        p.calculator.create_material('B')
        p.calculator.update_material('B', real=6.908, imag=-0.278)
        p.calculator.create_material('B2')
        p.calculator.update_material('B2', real=16.908, imag=-10.278)
        p.calculator.create_layer('B_layer', 'B')
        p.calculator.update_layer('B_layer', thick=10.0, rough=1.2)
        p.calculator.create_layer('B2_layer', 'B2')
        p.calculator.update_layer('B2_layer', thick=1.0, rough=0.2)
        p.calculator.create_item('ML')
        p.calculator.add_layer('ML', 'B_layer')
        p.calculator.add_layer('ML', 'B2_layer')
        p.calculator.create_item('ML2')
        p.calculator.add_layer('ML2', 'B2_layer')
        p.calculator.create_model()
        p.add_item_to_model('ML')
        p.add_item_to_model('ML2')
        assert_equal(len(p.calculator.storage['model'].structure.components),
                     2)
        assert_equal(
            len(p.calculator.storage['model'].structure.components[0].
                components), 2)
        assert_equal(
            len(p.calculator.storage['model'].structure.components[1].
                components), 1)
        p.remove_item_from_model('ML')
        assert_equal(len(p.calculator.storage['model'].structure.components),
                     1)
        assert_equal(
            len(p.calculator.storage['model'].structure.components[0].
                components), 1)

    def test_move_item_up(self):
        p = Refnx()
        p.calculator.create_material('B')
        p.calculator.update_material('B', real=6.908, imag=-0.278)
        p.calculator.create_material('B2')
        p.calculator.update_material('B2', real=16.908, imag=-10.278)
        p.calculator.create_layer('B_layer', 'B')
        p.calculator.update_layer('B_layer', thick=10.0, rough=1.2)
        p.calculator.create_layer('B2_layer', 'B2')
        p.calculator.update_layer('B2_layer', thick=1.0, rough=0.2)
        p.calculator.create_item('ML')
        p.calculator.create_item('ML2')
        p.calculator.add_layer('ML', 'B_layer')
        p.calculator.add_layer('ML', 'B2_layer')
        p.calculator.add_layer('ML2', 'B2_layer')
        p.calculator.add_layer('ML2', 'B_layer')
        p.calculator.create_model()
        p.calculator.add_item('ML')
        p.calculator.add_item('ML2')
        assert_equal(len(p.calculator.storage['model'].structure.components),
                     2)
        assert_equal(
            len(p.calculator.storage['model'].structure.components[0].
                components), 2)
        assert_equal(
            p.calculator.storage['model'].structure.components[1].repeats.
            value, 1)
        assert_equal(
            p.calculator.storage['model'].structure.components[1].
            components[0].thick.value, 1.0)
        assert_equal(
            p.calculator.storage['model'].structure.components[1].
            components[0].rough.value, 0.2)
        assert_equal(
            p.calculator.storage['model'].structure.components[1].
            components[0].sld.real.value, 16.908)
        assert_equal(
            p.calculator.storage['model'].structure.components[1].
            components[0].sld.imag.value, -10.278)
        p.move_item_up('ML2')
        assert_equal(
            p.calculator.storage['model'].structure.components[1].repeats.
            value, 1)
        assert_equal(
            p.calculator.storage['model'].structure.components[0].
            components[0].thick.value, 1.0)
        assert_equal(
            p.calculator.storage['model'].structure.components[0].
            components[0].rough.value, 0.2)
        assert_equal(
            p.calculator.storage['model'].structure.components[0].
            components[0].sld.real.value, 16.908)
        assert_equal(
            p.calculator.storage['model'].structure.components[0].
            components[0].sld.imag.value, -10.278)

    def test_move_item_down(self):
        p = Refnx()
        p.calculator.create_material('B')
        p.calculator.update_material('B', real=6.908, imag=-0.278)
        p.calculator.create_material('B2')
        p.calculator.update_material('B2', real=16.908, imag=-10.278)
        p.calculator.create_layer('B_layer', 'B')
        p.calculator.update_layer('B_layer', thick=10.0, rough=1.2)
        p.calculator.create_layer('B2_layer', 'B2')
        p.calculator.update_layer('B2_layer', thick=1.0, rough=0.2)
        p.calculator.create_item('ML')
        p.calculator.create_item('ML2')
        p.calculator.add_layer('ML', 'B_layer')
        p.calculator.add_layer('ML', 'B2_layer')
        p.calculator.add_layer('ML2', 'B2_layer')
        p.calculator.add_layer('ML2', 'B_layer')
        p.calculator.create_model()
        p.calculator.add_item('ML')
        p.calculator.add_item('ML2')
        assert_equal(len(p.calculator.storage['model'].structure.components),
                     2)
        assert_equal(
            len(p.calculator.storage['model'].structure.components[0].
                components), 2)
        assert_equal(
            p.calculator.storage['model'].structure.components[1].repeats.
            value, 1)
        assert_equal(
            p.calculator.storage['model'].structure.components[0].
            components[0].thick.value, 10.0)
        assert_equal(
            p.calculator.storage['model'].structure.components[0].
            components[0].rough.value, 1.2)
        assert_equal(
            p.calculator.storage['model'].structure.components[0].
            components[0].sld.real.value, 6.908)
        assert_equal(
            p.calculator.storage['model'].structure.components[0].
            components[0].sld.imag.value, -0.278)
        p.move_item_down('ML')
        assert_equal(
            p.calculator.storage['model'].structure.components[0].repeats.
            value, 1)
        assert_equal(
            p.calculator.storage['model'].structure.components[1].
            components[0].thick.value, 10.0)
        assert_equal(
            p.calculator.storage['model'].structure.components[1].
            components[0].rough.value, 1.2)
        assert_equal(
            p.calculator.storage['model'].structure.components[1].
            components[0].sld.real.value, 6.908)
        assert_equal(
            p.calculator.storage['model'].structure.components[1].
            components[0].sld.imag.value, -0.278)

    def test_get_model_value(self):
        p = Refnx()
        p.calculator.create_material('B')
        p.calculator.update_material('B', real=6.908, imag=-0.278)
        p.calculator.create_material('B2')
        p.calculator.update_material('B2', real=16.908, imag=-10.278)
        p.calculator.create_layer('B_layer', 'B')
        p.calculator.update_layer('B_layer', thick=10.0, rough=1.2)
        p.calculator.create_layer('B2_layer', 'B2')
        p.calculator.update_layer('B2_layer', thick=1.0, rough=0.2)
        p.calculator.create_item('ML')
        p.calculator.add_layer('ML', 'B_layer')
        p.calculator.add_layer('ML', 'B2_layer')
        p.calculator.create_model()
        p.calculator.add_item('ML')
        p.calculator.update_model(scale=2, bkg=1e-3, dq=2.0)
        assert_almost_equal(p.get_model_value('scale'), 2)
        assert_almost_equal(p.get_model_value('bkg'), 1e-3)
        assert_almost_equal(p.get_model_value('dq'), 2.0)

    def test_set_model_value(self):
        p = Refnx()
        p.calculator.create_material('B')
        p.calculator.update_material('B', real=6.908, imag=-0.278)
        p.calculator.create_material('B2')
        p.calculator.update_material('B2', real=16.908, imag=-10.278)
        p.calculator.create_layer('B_layer', 'B')
        p.calculator.update_layer('B_layer', thick=10.0, rough=1.2)
        p.calculator.create_layer('B2_layer', 'B2')
        p.calculator.update_layer('B2_layer', thick=1.0, rough=0.2)
        p.calculator.create_item('ML')
        p.calculator.add_layer('ML', 'B_layer')
        p.calculator.add_layer('ML', 'B2_layer')
        p.calculator.create_model()
        p.calculator.add_item('ML')
        p.set_model_value('scale', 2)
        p.set_model_value('background', 1e-3)
        p.set_model_value('resolution', 2.0)

    def test_fit_func(self):
        p = Refnx()
        p.calculator.create_material('Material1')
        p.calculator.update_material('Material1', real=0.000, imag=0.000)
        p.calculator.create_material('Material2')
        p.calculator.update_material('Material2', real=2.000, imag=0.000)
        p.calculator.create_material('Material3')
        p.calculator.update_material('Material3', real=4.000, imag=0.000)
        p.calculator.create_layer('Layer1', 'Material1')
        p.calculator.update_layer('Layer1', thick=0.0, rough=0.0)
        p.calculator.create_layer('Layer2', 'Material2')
        p.calculator.update_layer('Layer2', thick=10.0, rough=1.0)
        p.calculator.create_layer('Layer3', 'Material3')
        p.calculator.update_layer('Layer3', thick=0.0, rough=1.0)
        p.calculator.create_model()
        p.calculator.add_item('Layer1')
        p.calculator.add_item('Layer2')
        p.calculator.add_item('Layer3')
        q = np.linspace(0.001, 0.3, 10)
        expected = [
            9.99956517e-01, 2.16286891e-03, 1.14086254e-04, 1.93031759e-05,
            4.94188894e-06, 1.54191953e-06, 5.45592112e-07, 2.26619392e-07,
            1.26726993e-07, 1.01842852e-07
        ]
        assert_almost_equal(p.fit_func(q), expected)

    def test_sld_profile(self):
        p = Refnx()
        p.calculator.create_material('Material1')
        p.calculator.update_material('Material1', real=0.000, imag=0.000)
        p.calculator.create_material('Material2')
        p.calculator.update_material('Material2', real=2.000, imag=0.000)
        p.calculator.create_material('Material3')
        p.calculator.update_material('Material3', real=4.000, imag=0.000)
        p.calculator.create_layer('Layer1', 'Material1')
        p.calculator.update_layer('Layer1', thick=0.0, rough=0.0)
        p.calculator.create_layer('Layer2', 'Material2')
        p.calculator.update_layer('Layer2', thick=10.0, rough=1.0)
        p.calculator.create_layer('Layer3', 'Material3')
        p.calculator.update_layer('Layer3', thick=0.0, rough=1.0)
        p.calculator.create_model()
        p.calculator.add_item('Layer1')
        p.calculator.add_item('Layer2')
        p.calculator.add_item('Layer3')
        assert_almost_equal(p.sld_profile()[1][0], 0)
        assert_almost_equal(p.sld_profile()[1][-1], 4)
