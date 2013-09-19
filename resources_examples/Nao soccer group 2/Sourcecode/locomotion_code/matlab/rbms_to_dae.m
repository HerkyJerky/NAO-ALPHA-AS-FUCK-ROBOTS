function [nn] = rbms_to_dae(rbms, xtrain, xvalid, xtest)
% innermost rbm last
n = length(rbms);
nhs = zeros(1, 2 * n - 1);
for i = 1:n
    nhs(i) = rbms{i}.nh;
    nhs(2 * n - i) = rbms{i}.nh;
end
nn = feedforwardnet(nhs);
nn = configure(nn, xtrain', xtrain');
for i = 1:n
    nn.layers{i}.transferFcn = 'logsig';
    nn.layers{2 * n - i + 1}.transferFcn = 'logsig';
    
    rbm = rbms{i};

    if i == 1
        nn.IW{1} = rbm.W';
    else
        nn.LW{i, i - 1} = rbm.W';
    end
    
    nn.LW{2 * n - i + 1, 2 * n - i} = rbm.W;
    
    nn.b{i} = rbm.bh';
    nn.b{2 * n - i + 1} = rbm.bv';
end
% maybe make the code units linear:
%nn.layers{n}.transferFcn = 'purelin';
% maybe make the input and output units linear? probably should have
% trained them as gaussians then

xall = [xtrain; xvalid; xtest];

nn.trainFcn = 'traingd';            %# training function
nn.trainParam.epochs = 1000;        %# max number of iterations
nn.trainParam.lr = 0.05;            %# learning rate
nn.performFcn = 'mse';              %# mean-squared error function
nn.divideFcn = 'divideblock';        %# how to divide data
nn.divideParam.trainRatio = size(xtrain, 1) / size(xall, 1); %# training set
nn.divideParam.valRatio   = size(xvalid, 1) / size(xall, 1);   %# validation set
nn.divideParam.testRatio  = size(xtest,  1) / size(xall, 1);  %# testing set
end
