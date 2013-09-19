function [handle, collage] = rbm_plot_reconstructions(rbm, v)
    v = rbm_down(rbm, rbm_up(rbm, v));
    [handle, collage] = plot_patches(v);
end
