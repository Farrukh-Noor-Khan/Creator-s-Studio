# agents/video_agent.py
import pygame
import os
import subprocess

class VideoAgent:
    def __init__(self):
        self.output_dir = "assets"
        self.frames_dir = "assets/frames"
        os.makedirs(self.frames_dir, exist_ok=True)

    def generate_video(self, audio_path: str, script_text: str, output_path: str = "assets/final_video.mp4") -> str:
        try:
            pygame.init()

            # Setup Pygame with standard 9:16 resolution
            width, height = 1080, 1920  # Standard 9:16 for TikTok/YouTube Shorts
            fps = 24
            background_color = (0, 0, 0)
            text_color = (255, 255, 255)
            font = pygame.font.SysFont('arial', 60, bold=True)  # Larger and bold text

            screen = pygame.Surface((width, height))

            # Get duration from audio
            probe = subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', audio_path])
            duration = float(probe)
            frame_count = int(duration * fps)

            # Split script into words for captions
            words = script_text.split()
            total_words = len(words)
            frames_per_word = max(1, frame_count // total_words)  # Minimum 1 frame per word

            # Interactive area
            interactive_x, interactive_y = width - 300, height - 100
            interactive_w, interactive_h = 250, 50

            # Generate animated frames with caption-style text
            current_word_idx = 0
            for i in range(frame_count):
                screen.fill(background_color)

                # Display captions: show current word with fade effect
                if current_word_idx < total_words:
                    progress = (i % frames_per_word) / frames_per_word
                    alpha = min(255, int(255 * progress)) if progress < 0.5 else int(255 * (1 - progress))  # Fade in/out
                    if i % frames_per_word == 0 and i // frames_per_word < total_words:
                        current_word_idx = i // frames_per_word
                    if current_word_idx < total_words:
                        rendered_text = font.render(words[current_word_idx], True, text_color)
                        rendered_text.set_alpha(alpha)
                        text_rect = rendered_text.get_rect(center=(width // 2, height // 2 + 150))  # Adjusted position for larger text
                        screen.blit(rendered_text, text_rect)

                # Interactive cue
                if i % (fps * 2) < fps:
                    pygame.draw.rect(screen, (100, 100, 255), (interactive_x, interactive_y, interactive_w, interactive_h), 2)
                    button_text = font.render("Tap Here!", True, (100, 100, 255))
                    screen.blit(button_text, (interactive_x + 50, interactive_y + 10))

                pygame.image.save(screen, f"{self.frames_dir}/frame_{i:04d}.png")

            # Use ffmpeg to combine frames into video
            os.system(f'ffmpeg -framerate {fps} -i {self.frames_dir}/frame_%04d.png -i {audio_path} -c:v libx264 -pix_fmt yuv420p -c:a aac -map 0:v:0 -map 1:a:0 -shortest {output_path}')

            # Clean up
            for file in os.listdir(self.frames_dir):
                os.remove(os.path.join(self.frames_dir, file))
            os.rmdir(self.frames_dir)

            print(f"Video generated: {output_path}")
            return output_path

        except Exception as e:
            print(f"❌ Error in VideoAgent: {e}")
            return audio_path

# Test
if __name__ == "__main__":
    agent = VideoAgent()
    # agent.generate_video("assets/narration.mp3", "This is a test script text.")