dataset = load('linewalk');

[dataset.y, ymap] = rbm_preprocess(dataset.y);

ytrain = dataset.y(1:24999, :);
yvalid = dataset.y(25000:end, :);

yperm = randperm(size(ytrain, 1));
ytrain = ytrain(yperm, :);

options = [];
options.learning_rate = 0.00001;
options.batch_size = 30;
options.chain_length = 1;
options.sparsity_cost = 0.5;
options.desired_sparsity = 0.1;
options.sparsity_estimate_decay = 0.9;
options.weight_cost = 0.00001;
options.initial_momentum = 0.5;
options.final_momentum = 0.9;
options.overfitting_estimate_decay = 0.9;
options.overfitting_threshold = 1; % no idea here
options.validation_interval = 5;

rbm = rbm_create(size(ytrain, 2), 32);
rbm.sample_up = @identity;
rbm.sample_down = @identity;
rbm.sigmoid_up = @rbm_sigmoid;
rbm.sigmoid_down = @identity;
rbm = rbm_initialize_parameters(rbm, ytrain, options);

[rbm, continuation] = rbm_train(rbm, ytrain, yvalid, 300, options);
