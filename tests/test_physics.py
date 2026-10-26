"""Independent limiting cases, paper-number checks, and physical invariants."""

from __future__ import annotations

import math
import unittest

import numpy as np

from siv_study.charge_states import derive_intercepts, formation_energy, stable_intervals
from siv_study.hyperfine import axial_tensor, decompose_tensor, tensor_metrics
from siv_study.parity_mixing import borrowed_intensity_analytic, mixing_solution, parity_permits


class ChargeStatePhysicsTests(unittest.TestCase):
    def setUp(self):
        self.intercepts = derive_intercepts(1.43, 2.14)

    def test_reported_crossings_and_derived_intercepts(self):
        self.assertAlmostEqual(self.intercepts[0], 0.0)
        self.assertAlmostEqual(self.intercepts[-1], 1.43)
        self.assertAlmostEqual(self.intercepts[-2], 3.57)
        self.assertAlmostEqual(formation_energy(1.43, 0, self.intercepts[0]), 0.0)
        self.assertAlmostEqual(formation_energy(1.43, -1, self.intercepts[-1]), 0.0)
        self.assertAlmostEqual(formation_energy(2.14, -1, self.intercepts[-1]), -0.71)
        self.assertAlmostEqual(formation_energy(2.14, -2, self.intercepts[-2]), -0.71)

    def test_inactive_nonadjacent_crossing_is_not_a_boundary(self):
        intervals = stable_intervals(self.intercepts)
        self.assertEqual([item["charge"] for item in intervals], [0, -1, -2])
        self.assertEqual(len(intervals), 3)
        self.assertAlmostEqual(intervals[0]["fermi_min_eV"], 0.0)
        self.assertAlmostEqual(intervals[0]["fermi_max_eV"], 1.43)
        self.assertAlmostEqual(intervals[1]["fermi_max_eV"], 2.14)
        self.assertAlmostEqual(intervals[2]["fermi_max_eV"], 5.34)
        self.assertAlmostEqual(formation_energy(1.785, -2, self.intercepts[-2]), 0.0)
        self.assertAlmostEqual(formation_energy(1.785, -1, self.intercepts[-1]), -0.355)

    def test_expected_states_on_either_side_of_crossings(self):
        cases = [(0.0, 0), (1.429, 0), (1.431, -1), (2.139, -1), (2.141, -2), (5.34, -2)]
        for fermi, expected in cases:
            with self.subTest(fermi=fermi):
                actual = min(self.intercepts, key=lambda q: formation_energy(fermi, q, self.intercepts[q]))
                self.assertEqual(actual, expected)

    def test_energy_zero_does_not_change_charge_stability(self):
        shifted = derive_intercepts(1.43, 2.14, neutral_offset=12.3)
        original_intervals = stable_intervals(self.intercepts)
        shifted_intervals = stable_intervals(shifted)
        self.assertEqual([item["charge"] for item in shifted_intervals], [0, -1, -2])
        for original, changed in zip(original_intervals, shifted_intervals):
            self.assertAlmostEqual(original["fermi_min_eV"], changed["fermi_min_eV"])
            self.assertAlmostEqual(original["fermi_max_eV"], changed["fermi_max_eV"])

    def test_charge_sets_the_response_to_fermi_level(self):
        fermi = np.array([0.2, 0.7, 1.2])
        # Raising E_F by 0.5 eV lowers a doubly negative formation line by 1 eV.
        values = formation_energy(fermi, -2, 3.57)
        np.testing.assert_allclose(np.diff(values), [-1.0, -1.0], atol=1e-14)

    def test_invalid_and_nonfinite_input_is_rejected(self):
        for first, second in [(2.14, 1.43), (0.0, 2.14), (1.43, math.nan), (math.inf, 2.14)]:
            with self.subTest(first=first, second=second), self.assertRaises(ValueError):
                derive_intercepts(first, second)
        with self.assertRaises(ValueError):
            formation_energy([0.0, math.nan], -1, 1.43)
        with self.assertRaises(ValueError):
            formation_energy(1.0, True, 1.43)
        with self.assertRaises(ValueError):
            stable_intervals({}, 0.0, 5.34)


class ParityAndMixingPhysicsTests(unittest.TestCase):
    def test_odd_dipole_needs_opposite_state_parity(self):
        self.assertFalse(parity_permits("g", "g"))
        self.assertFalse(parity_permits("u", "u"))
        self.assertTrue(parity_permits("g", "u"))
        self.assertTrue(parity_permits("u", "g"))
        # An even operator instead has the complementary necessary condition.
        self.assertTrue(parity_permits("g", "g", operator="g"))
        self.assertFalse(parity_permits("g", "u", operator="g"))

    def test_uncoupled_limit_has_exact_dark_and_bright_states(self):
        result = mixing_solution(0.0)
        self.assertEqual(result["lower_energy_over_Delta"], 0.0)
        self.assertEqual(result["upper_energy_over_Delta"], 1.0)
        self.assertEqual(result["lower_borrowed_intensity"], 0.0)
        self.assertEqual(result["upper_bright_intensity"], 1.0)

    def test_known_half_coupling_solution(self):
        result = mixing_solution(0.5)
        self.assertAlmostEqual(result["lower_energy_over_Delta"], (1.0 - math.sqrt(2.0)) / 2.0)
        self.assertAlmostEqual(result["upper_energy_over_Delta"], (1.0 + math.sqrt(2.0)) / 2.0)
        self.assertAlmostEqual(result["lower_borrowed_intensity"], 0.14644660940672624)
        self.assertAlmostEqual(borrowed_intensity_analytic(0.5), 0.14644660940672624)

    def test_reversal_of_odd_perturbation_preserves_strength(self):
        for coupling in [0.001, 0.13, 0.5, 1.0]:
            with self.subTest(coupling=coupling):
                positive = mixing_solution(coupling)
                negative = mixing_solution(-coupling)
                self.assertAlmostEqual(positive["lower_borrowed_intensity"], negative["lower_borrowed_intensity"])
                self.assertAlmostEqual(positive["lower_energy_over_Delta"], negative["lower_energy_over_Delta"])
                self.assertAlmostEqual(positive["lower_borrowed_intensity"] + positive["upper_bright_intensity"], 1.0)
                self.assertLess(positive["max_eigenvector_residual"], 1e-12)
                self.assertLess(positive["max_orthogonality_error"], 1e-12)

    def test_small_coupling_intensity_is_quadratic(self):
        larger = mixing_solution(0.001)["lower_borrowed_intensity"]
        smaller = mixing_solution(0.0001)["lower_borrowed_intensity"]
        # Ten times less amplitude gives approximately 100 times less strength.
        self.assertAlmostEqual(larger / smaller, 100.0, delta=0.001)
        self.assertAlmostEqual(smaller / 1e-8, 1.0, delta=1e-6)
        self.assertAlmostEqual(borrowed_intensity_analytic(0.0001), smaller, delta=1e-18)

    def test_invalid_parity_or_coupling_is_rejected(self):
        with self.assertRaises(ValueError):
            parity_permits("g", "odd")
        for coupling in [math.nan, math.inf, 2.0, True]:
            with self.subTest(coupling=coupling), self.assertRaises(ValueError):
                mixing_solution(coupling)
            with self.subTest(analytic=coupling), self.assertRaises(ValueError):
                borrowed_intensity_analytic(coupling)


class HyperfinePhysicsTests(unittest.TestCase):
    def test_axial_frame_and_quarter_turn(self):
        np.testing.assert_allclose(axial_tensor(66.2, 30.2), np.diag([30.2, 30.2, 66.2]), atol=1e-12)
        np.testing.assert_allclose(axial_tensor(66.2, 30.2, theta_deg=90.0), np.diag([66.2, 30.2, 30.2]), atol=1e-12)

    def test_analytic_45_degree_tensor(self):
        # At 45 degrees the parallel-axis projector has xx=xz=zx=zz=1/2.
        tensor = axial_tensor(8.0, 2.0, theta_deg=45.0)
        np.testing.assert_allclose(tensor, [[5.0, 0.0, 3.0], [0.0, 2.0, 0.0], [3.0, 0.0, 5.0]], atol=1e-12)
        isotropic, traceless = decompose_tensor(tensor)
        self.assertAlmostEqual(isotropic, 4.0)
        self.assertAlmostEqual(float(np.trace(traceless)), 0.0)
        np.testing.assert_allclose(traceless + isotropic * np.eye(3), tensor, atol=1e-12)

    def test_paper_isotropic_averages_and_anisotropy(self):
        carbon = tensor_metrics(axial_tensor(66.2, 30.2, 35.3))
        silicon = tensor_metrics(axial_tensor(76.3, 78.9, 0.0))
        self.assertAlmostEqual(carbon["a_iso_MHz"], 42.2)
        self.assertAlmostEqual(silicon["a_iso_MHz"], 78.03333333333333)
        self.assertAlmostEqual(carbon["principal_span_MHz"], 36.0)
        self.assertAlmostEqual(silicon["principal_span_MHz"], 2.6)
        self.assertLess(silicon["anisotropic_frobenius_norm_MHz"], carbon["anisotropic_frobenius_norm_MHz"])

    def test_parallel_smaller_than_perp_is_not_mislabeled(self):
        silicon = tensor_metrics(axial_tensor(76.3, 78.9))
        np.testing.assert_allclose(silicon["principal_values_MHz"], [76.3, 78.9, 78.9], atol=1e-12)
        self.assertGreater(silicon["anisotropic_frobenius_norm_MHz"], 0.0)

    def test_coordinate_rotation_preserves_tensor_invariants(self):
        original = axial_tensor(68.0, 28.0, theta_deg=34.6)
        # A cyclic permutation is an independent exact orthogonal coordinate change.
        rotation = np.array([[0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [1.0, 0.0, 0.0]])
        before = tensor_metrics(original)
        after = tensor_metrics(rotation @ original @ rotation.T)
        self.assertAlmostEqual(before["a_iso_MHz"], after["a_iso_MHz"])
        self.assertAlmostEqual(before["anisotropic_frobenius_norm_MHz"], after["anisotropic_frobenius_norm_MHz"])
        np.testing.assert_allclose(before["principal_values_MHz"], after["principal_values_MHz"], atol=1e-12)

    def test_isotropic_and_signed_tensors_are_supported(self):
        iso = tensor_metrics(axial_tensor(-2.0, -2.0, 33.0, 125.0))
        self.assertAlmostEqual(iso["a_iso_MHz"], -2.0)
        self.assertAlmostEqual(iso["anisotropic_frobenius_norm_MHz"], 0.0)

    def test_invalid_tensor_or_angles_are_rejected(self):
        for matrix in [np.zeros((2, 2)), np.full((3, 3), math.nan), np.triu(np.ones((3, 3)))]:
            with self.subTest(matrix=str(matrix)), self.assertRaises(ValueError):
                decompose_tensor(matrix)
        for theta, phi in [(-1.0, 0.0), (181.0, 0.0), (0.0, 360.0), (math.nan, 0.0)]:
            with self.subTest(theta=theta, phi=phi), self.assertRaises(ValueError):
                axial_tensor(1.0, 2.0, theta, phi)


if __name__ == "__main__":
    unittest.main()
