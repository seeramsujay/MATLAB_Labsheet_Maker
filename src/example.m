% Example MATLAB/Octave Script
disp('Generating a sine wave plot...');

t = 0:0.01:2*pi;
y = sin(t);

% Plot and save as PNG using the prefix matching the script name
figure('visible', 'off');
plot(t, y, 'r-', 'LineWidth', 2);
title('Example Sine Wave');
xlabel('Time (s)');
ylabel('Amplitude');
grid on;

% Save plot next to the script
print('example_plot.png', '-dpng', '-r150');
disp('Done!');
