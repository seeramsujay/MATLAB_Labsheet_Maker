% Convolution with Sinc - Task B1
n = -20:20;
fc = 0.15;
h = sinc(2*fc*n);

N = 100;  m = 0:N-1;
x_slow = sin(2*pi*0.05*m);
x_fast = sin(2*pi*0.35*m);
x = x_slow + x_fast;

y = conv(x, h, 'same');

figure;
subplot(3,1,1); plot(m, x);      title('x[n] = slow + fast sine');        grid on;
subplot(3,1,2); plot(m, x_slow); title('x_slow[n] alone (reference)');   grid on;
subplot(3,1,3); plot(m, y);      title('y[n] = x[n] * h[n] (filtered)'); grid on;
print('convolution_plot1.png', '-dpng', '-r300');

% fc = 0.4 - above both frequencies
fc = 0.4;
h = sinc(2*fc*n);
y = conv(x, h, 'same');

figure;
subplot(3,1,1); plot(m, x);      title('x[n] slow+fast fc=0.4');         grid on;
subplot(3,1,2); plot(m, x_fast); title('x_fast[n] alone (reference)');    grid on;
subplot(3,1,3); plot(m, y);      title('y[n] filtered fc=0.4');           grid on;
print('convolution_plot2.png', '-dpng', '-r300');

% fc = 0.02 - below both frequencies
fc = 0.02;
h = sinc(2*fc*n);
y = conv(x, h, 'same');

figure;
subplot(3,1,1); plot(m, x);      title('x[n] slow+fast fc=0.02');         grid on;
subplot(3,1,2); plot(m, x_slow); title('x_slow[n] alone (reference)');    grid on;
subplot(3,1,3); plot(m, y);      title('y[n] filtered fc=0.02');           grid on;
print('convolution_plot3.png', '-dpng', '-r300');
