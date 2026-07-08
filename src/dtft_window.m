% DTFT of Rectangular Window - Task C2
w = linspace(-pi, pi, 1024);
figure;
hold on;

for N = [8, 16, 32, 64]
  n = 0:N-1;
  x_rect = ones(1, N);
  X = zeros(1, length(w));
  for k = 1:length(w)
    sumval = 0;
    for i = 1:N
      sumval = sumval + x_rect(i) * exp(-j * w(k) * n(i));
    end
    X(k) = sumval;
  end
  plot(w/pi, abs(X));
end

hold off;
legend('N=8','N=16','N=32','N=64');
title('DTFT Magnitude of Rectangular Windows');
xlabel('omega/pi'); ylabel('|X(e^j^omega)|'); grid on;
print('dtft_window_plot1.png', '-dpng', '-r300');
