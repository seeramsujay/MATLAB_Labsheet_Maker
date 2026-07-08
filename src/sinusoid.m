% Sinusoid experiments - Task A1
fs = 1000;
T = 1;
t = 0:1/fs:T-1/fs;

% Part 1: A=1, f0=10, phi=0
A = 1;
f0 = 10;
phi = 0;
x_sine = A * sin(2*pi*f0*t + phi);

figure;
plot(t, x_sine);
title('Sinusoidal Signal A=1 f0=10 phi=0');
xlabel('Time (s)'); ylabel('Amplitude');
grid on;
print('sinusoid_plot1.png', '-dpng', '-r300');

% Count cycles: find zero crossings
zerocross = 0;
for i = 2:length(x_sine)
  if x_sine(i-1) <= 0 && x_sine(i) > 0
    zerocross = zerocross + 1;
  end
end
cycles = zerocross;
disp(['Cycles for f0=10: ' num2str(cycles)]);

% Part 2: f0=50
f0 = 50;
x_sine = A * sin(2*pi*f0*t + phi);

figure;
plot(t, x_sine);
title('Sinusoidal Signal A=1 f0=50 phi=0');
xlabel('Time (s)'); ylabel('Amplitude');
grid on;
print('sinusoid_plot2.png', '-dpng', '-r300');

zerocross = 0;
for i = 2:length(x_sine)
  if x_sine(i-1) <= 0 && x_sine(i) > 0
    zerocross = zerocross + 1;
  end
end
cycles = zerocross;
disp(['Cycles for f0=50: ' num2str(cycles)]);

% Part 3: phi=pi/4
f0 = 10;
phi = pi/4;
x_sine = A * sin(2*pi*f0*t + phi);

figure;
plot(t, x_sine);
title('Sinusoidal Signal A=1 f0=10 phi=pi/4');
xlabel('Time (s)'); ylabel('Amplitude');
grid on;
print('sinusoid_plot3.png', '-dpng', '-r300');

% Part 4: Combine two sinusoids
f1 = 10;
f2 = 50;
x1 = sin(2*pi*f1*t);
x2 = sin(2*pi*f2*t);
x = x1 + x2;

figure;
plot(t, x);
title('Sum of Two Sinusoids 10Hz + 50Hz');
xlabel('Time (s)'); ylabel('Amplitude');
grid on;
print('sinusoid_plot4.png', '-dpng', '-r300');
