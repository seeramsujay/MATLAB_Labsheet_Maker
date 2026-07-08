% Sinc Function - Task A3
n = -20:20;

% fc = 0.2
fc = 0.2;
h = sinc(2*fc*n);

figure;
stem(n, h, 'filled', 'MarkerSize', 4);
title(['Sinc Function fc = ' num2str(fc)]);
xlabel('n'); ylabel('h[n]'); grid on;
print('sincfunc_plot1.png', '-dpng', '-r300');

% Find peak
[maxval maxidx] = max(h);
disp(['fc=0.2: Peak at n=' num2str(n(maxidx)) ' value=' num2str(maxval)]);

% Check zero crossings
for k = 1:5
  idx = round(1/(2*fc) * k) + 21;
  if idx <= length(h)
    disp(['fc=0.2: h[' num2str(k) '/(2*fc)] = ' num2str(h(idx))]);
  end
end

% Compare continuous vs discrete
figure;
t_cont = -20:0.05:20;
h_cont = sinc(2*fc*t_cont);
plot(t_cont, h_cont, 'b-'); hold on;
stem(n, h, 'filled', 'r', 'MarkerSize', 4);
legend('continuous envelope', 'discrete samples');
title('Sinc continuous vs discrete fc=0.2'); grid on;
print('sincfunc_plot2.png', '-dpng', '-r300');

% fc = 0.4
fc = 0.4;
h = sinc(2*fc*n);

figure;
stem(n, h, 'filled', 'MarkerSize', 4);
title(['Sinc Function fc = ' num2str(fc)]);
xlabel('n'); ylabel('h[n]'); grid on;
print('sincfunc_plot3.png', '-dpng', '-r300');

figure;
t_cont = -20:0.05:20;
h_cont = sinc(2*fc*t_cont);
plot(t_cont, h_cont, 'b-'); hold on;
stem(n, h, 'filled', 'r', 'MarkerSize', 4);
legend('continuous envelope', 'discrete samples');
title('Sinc continuous vs discrete fc=0.4'); grid on;
print('sincfunc_plot4.png', '-dpng', '-r300');
