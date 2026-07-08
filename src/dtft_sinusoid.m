% DTFT of Sinusoid - Task C1
N = 32;
n = 0:N-1;
f0 = 0.1;
x = sin(2*pi*f0*n);

w = linspace(-pi, pi, 1024);
X = zeros(1, length(w));

for k = 1:length(w)
  sumval = 0;
  for i = 1:N
    sumval = sumval + x(i) * exp(-j * w(k) * n(i));
  end
  X(k) = sumval;
end

figure;
subplot(3,1,1);
stem(n, x, 'filled', 'MarkerSize', 4);
title('x[n] discrete sinusoid f0=0.1');
xlabel('n'); ylabel('x[n]'); grid on;

subplot(3,1,2);
plot(w/pi, abs(X));
title('|X(e^j^omega)| Magnitude Spectrum');
xlabel('omega/pi'); ylabel('Magnitude'); grid on;

subplot(3,1,3);
plot(w/pi, angle(X));
title('angle(X(e^j^omega)) Phase Spectrum');
xlabel('omega/pi'); ylabel('Phase (rad)'); grid on;
print('dtft_sinusoid_plot1.png', '-dpng', '-r300');

% f0 = 0.25
f0 = 0.25;
x = sin(2*pi*f0*n);
X = zeros(1, length(w));
for k = 1:length(w)
  sumval = 0;
  for i = 1:N
    sumval = sumval + x(i) * exp(-j * w(k) * n(i));
  end
  X(k) = sumval;
end

figure;
subplot(3,1,1);
stem(n, x, 'filled', 'MarkerSize', 4);
title('x[n] discrete sinusoid f0=0.25');
xlabel('n'); ylabel('x[n]'); grid on;

subplot(3,1,2);
plot(w/pi, abs(X));
title('|X(e^j^omega)| Magnitude Spectrum');
xlabel('omega/pi'); ylabel('Magnitude'); grid on;

subplot(3,1,3);
plot(w/pi, angle(X));
title('angle(X(e^j^omega)) Phase Spectrum');
xlabel('omega/pi'); ylabel('Phase (rad)'); grid on;
print('dtft_sinusoid_plot2.png', '-dpng', '-r300');

% N = 8
N = 8;
n = 0:N-1;
x = sin(2*pi*f0*n);
X = zeros(1, length(w));
for k = 1:length(w)
  sumval = 0;
  for i = 1:N
    sumval = sumval + x(i) * exp(-j * w(k) * n(i));
  end
  X(k) = sumval;
end

figure;
subplot(2,1,1);
stem(n, x, 'filled', 'MarkerSize', 4);
title('x[n] N=8 f0=0.25');
xlabel('n'); ylabel('x[n]'); grid on;

subplot(2,1,2);
plot(w/pi, abs(X));
title('|X(e^j^omega)| N=8');
xlabel('omega/pi'); ylabel('Magnitude'); grid on;
print('dtft_sinusoid_plot3.png', '-dpng', '-r300');

% N = 128
N = 128;
n = 0:N-1;
x = sin(2*pi*f0*n);
X = zeros(1, length(w));
for k = 1:length(w)
  sumval = 0;
  for i = 1:N
    sumval = sumval + x(i) * exp(-j * w(k) * n(i));
  end
  X(k) = sumval;
end

figure;
subplot(2,1,1);
stem(n, x, 'filled', 'MarkerSize', 4);
title('x[n] N=128 f0=0.25');
xlabel('n'); ylabel('x[n]'); grid on;

subplot(2,1,2);
plot(w/pi, abs(X));
title('|X(e^j^omega)| N=128');
xlabel('omega/pi'); ylabel('Magnitude'); grid on;
print('dtft_sinusoid_plot4.png', '-dpng', '-r300');
