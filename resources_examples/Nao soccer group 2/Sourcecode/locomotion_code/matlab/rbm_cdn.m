function [dfe_W, dfe_bv, dfe_bh, mean_ph] = rbm_cdn(rbm, n, v)
    ph = rbm_up(rbm, v);
    h = rbm.sample_up(ph);

    % compute mean activations on the batch to estimate (non)sparsity
    mean_ph = mean(ph, 1);

    % temporarily need a tensor to accomodate dW for each sample in the
    % batch.  if the batch size is one (i.e., v is a vector), the below
    % is equivalent to dfe_W_data = ph * v';
    dfe_W_data = reshape(mean(etprod('kij', ph,'kj', v,'ki'), 1), size(rbm.W));
    dfe_bv_data = mean(v, 1);
    dfe_bh_data = mean(h, 1);
    
    for i = 1:n
        pv = rbm_down(rbm, h);
        v = rbm.sample_down(pv);
        ph = rbm_up(rbm, v);
        if i ~= n
            h = rbm.sample_up(ph);
        end
    end

    dfe_W_recon = reshape(mean(etprod('kij', ph,'kj', v,'ki'), 1), size(rbm.W));
    dfe_bv_recon = mean(v, 1);
    dfe_bh_recon = mean(ph, 1);
    
    dfe_W = dfe_W_data - dfe_W_recon;
    dfe_bv = dfe_bv_data - dfe_bv_recon;
    dfe_bh = dfe_bh_data - dfe_bh_recon;
end
