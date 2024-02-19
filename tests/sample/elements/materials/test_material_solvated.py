import pytest
import EasyReflectometry.sample.elements.materials.material_mixture
import EasyReflectometry.sample.elements.materials.material_solvated

from unittest.mock import MagicMock
from EasyReflectometry.sample.elements.materials.material_solvated import MaterialSolvated

class TestMaterialMixture():

    @pytest.fixture
    def material_solvated(self, monkeypatch) -> MaterialSolvated:
        self.mock_material = MagicMock()
        self.mock_material.name = 'material'
        self.mock_solvent = MagicMock()
        self.mock_solvent.name = 'solvent'
        self.mock_solvation = MagicMock()
        self.mock_interface = MagicMock()
        self.mock_Parameter = MagicMock()
        self.mock_FunctionalConstraint = MagicMock()
        monkeypatch.setattr(EasyReflectometry.sample.elements.materials.material_mixture, 'Parameter', self.mock_Parameter)
        monkeypatch.setattr(EasyReflectometry.sample.elements.materials.material_mixture, 'FunctionalConstraint', self.mock_FunctionalConstraint)
        return MaterialSolvated(self.mock_material, self.mock_solvent, self.mock_solvation, name='name', interface=self.mock_interface)

    def test_init(self, material_solvated: MaterialSolvated) -> None:
        assert material_solvated.material_a == self.mock_material
        assert material_solvated.material_b == self.mock_solvent
        assert material_solvated.fraction == self.mock_solvation
        assert material_solvated.name == 'name'
        assert material_solvated.interface == self.mock_interface
        self.mock_interface.generate_bindings.call_count == 2

    def test_material(self, material_solvated: MaterialSolvated) -> None:
        assert material_solvated.material == self.mock_material

    def test_set_material(self, material_solvated: MaterialSolvated) -> None:
        new_material = MagicMock()
        new_material.name = 'new_material'
        material_solvated.material = new_material
        assert material_solvated.material == new_material
        assert material_solvated.name == 'new_material solvated in solvent'

    def test_solvent(self, material_solvated: MaterialSolvated) -> None:
        assert material_solvated.solvent == self.mock_solvent

    def test_set_solvent(self, material_solvated: MaterialSolvated) -> None:
        new_solvent = MagicMock()
        new_solvent.name = 'new_solvent'
        material_solvated.solvent = new_solvent
        assert material_solvated.solvent == new_solvent
        assert material_solvated.name == 'material solvated in new_solvent'

    def test_solvation(self, material_solvated: MaterialSolvated) -> None:
        assert material_solvated.solvation == self.mock_solvation

    def test_set_solvation(self, material_solvated: MaterialSolvated) -> None:
        material_solvated.solvation = 1.0
        assert material_solvated.solvation == 1.0
    
    def test_set_solvation_exception(self, material_solvated: MaterialSolvated) -> None:
        with pytest.raises(ValueError):
            material_solvated.solvation = 'not float'