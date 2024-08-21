import sys

import numpy as np
from lenstronomy.Extensions.Substructure.sensitivity import Sensitivity


class ClumpDetect(Sensitivity):
    """
    class with routines to make sensitivity maps
    """
    def __init__(self, kwargs_options, kwargs_data, kwargs_psf, kwargs_lens, kwargs_source,
                          kwargs_lens_light, kwargs_else):
        self.kwargs_options = kwargs_options
        self.kwargs_data = kwargs_data
        self.kwargs_lens = kwargs_lens
        self.kwargs_source = kwargs_source
        self.kwargs_psf = kwargs_psf
        self.kwargs_lens_light = kwargs_lens_light
        self.kwargs_else = kwargs_else

    def relative_chi2(self, theta_E_clump, r_trunc, x_clump, y_clump):
        """

        :param phi_E:
        :param r_trunc:
        :param x_clump:
        :param y_clump:
        :return:
        """
        image, param, residuals, image_smooth, param_smooth, residuals_smooth = self.detection(self.kwargs_options, self.kwargs_data, self.kwargs_lens, self.kwargs_source, self.kwargs_psf,
                                                                                               self.kwargs_lens_light, self.kwargs_else, x_clump, y_clump, theta_E_clump, r_trunc)
        chi2_clump, chi2_smooth = np.sum(np.array(residuals)**2, axis=1), np.sum(np.array(residuals_smooth)**2, axis=1)
        return chi2_clump, chi2_smooth

    def iterate_position(self, theta_E_clump, r_trunc, x_clump, y_clump, compute_bool):
        """

        :param theta_E_clump:
        :param r_trunc:
        :param x_clump:
        :param y_clump:
        :return:
        """
        n = len(x_clump)
        num_bands = self.num_bands(self.kwargs_data)
        print("number of positions to be computed: ", np.sum(compute_bool), "out of ", n)
        sys.stdout.flush()
        chi2_list_clump = np.zeros((n, num_bands))
        chi2_list_smooth = np.zeros((n, num_bands))
        p_i = 0
        for i in range(n):
            if compute_bool[i] == 1:
                chi2_list_clump[i], chi2_list_smooth[i] = self.relative_chi2(theta_E_clump, r_trunc, x_clump[i], y_clump[i])
                print(p_i)
                p_i += 1
                #sys.stdout.flush()
            else:
                chi2_list_clump[i], chi2_list_smooth[i] = np.zeros(num_bands), np.zeros(num_bands)
        return chi2_list_smooth, chi2_list_clump
