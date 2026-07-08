% Impulse Train - Task A2
N = 100;
n = 0:N-1;

% Part 1: T0 = 10
T0 = 10;
p = zeros(1, N);
p(1:T0:N) = 1;

figure;
stem(n, p, 'filled', 'MarkerSize', 4);
title(['Impulse Train T0 = ' num2str(T0)]);
xlabel('n'); ylabel('p[n]'); grid on;
ylim([-0.2 1.2]);
print('impulsetrain_plot1.png', '-dpng', '-r300');

num_imp = sum(p);
disp(['T0=10: Num impulses = ' num2str(num_imp)]);

% Part 2: T0 = 5
T0 = 5;
p = zeros(1, N);
p(1:T0:N) = 1;

figure;
stem(n, p, 'filled', 'MarkerSize', 4);
title(['Impulse Train T0 = ' num2str(T0)]);
xlabel('n'); ylabel('p[n]'); grid on;
ylim([-0.2 1.2]);
print('impulsetrain_plot2.png', '-dpng', '-r300');

num_imp = sum(p);
disp(['T0=5: Num impulses = ' num2str(num_imp)]);

% T0 = 20
T0 = 20;
p = zeros(1, N);
p(1:T0:N) = 1;

figure;
stem(n, p, 'filled', 'MarkerSize', 4);
title(['Impulse Train T0 = ' num2str(T0)]);
xlabel('n'); ylabel('p[n]'); grid on;
ylim([-0.2 1.2]);
print('impulsetrain_plot3.png', '-dpng', '-r300');

num_imp = sum(p);
disp(['T0=20: Num impulses = ' num2str(num_imp)]);

% Part 3: Multiply sinusoid by impulse train
T0 = 10;
p = zeros(1, N);
p(1:T0:N) = 1;
x = sin(2*pi*0.05*n);
x_sampled = x .* p;

figure;
subplot(3,1,1);
stem(n, x, 'filled', 'MarkerSize', 4);
title('Sinusoid x[n]');
xlabel('n'); ylabel('x[n]'); grid on;

subplot(3,1,2);
stem(n, p, 'filled', 'MarkerSize', 4);
title(['Impulse Train T0=' num2str(T0)]);
xlabel('n'); ylabel('p[n]'); grid on;
ylim([-0.2 1.2]);

subplot(3,1,3);
stem(n, x_sampled, 'filled', 'MarkerSize', 4);
title('Sampled Signal x[n] * p[n]');
xlabel('n'); ylabel('x_sampled'); grid on;
print('impulsetrain_plot4.png', '-dpng', '-r300');
