import os
import subprocess
import shutil
import pygame

# Set ImageMagick path (if needed by pygame or PIL, but not directly used here)
os.environ["IMAGEMAGICK_BINARY"] = r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"


class VideoAgent:
    def __init__(self):
        self.output_dir = "assets"
        self.frames_dir = os.path.join(self.output_dir, "frames")
        os.makedirs(self.frames_dir, exist_ok=True)

    def generate_video(self, audio_path: str, script_text: str, output_path: str = "assets/final_video.mp4") -> str:
        try:
            # Init pygame
            pygame.init()
            pygame.font.init()

            # Video settings
            width, height = 1080, 1920   # TikTok / Shorts vertical resolution
            fps = 24
            background_color = (0, 0, 0)
            text_color = (200, 200, 200)   # dim white for normal words
            highlight_color = (255, 255, 0)  # yellow highlight
            font = pygame.font.SysFont("arial", 70, bold=True)

            # Drawing surface
            screen = pygame.Surface((width, height))

            # Get audio duration using ffprobe
            probe = subprocess.check_output([
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                audio_path
            ])
            duration = float(probe)
            frame_count = int(duration * fps)

            # Prepare script text
            words = script_text.split()
            total_words = len(words)
            frames_per_word = max(1, frame_count // total_words)

            # Generate frames
            for i in range(frame_count):
                screen.fill(background_color)

                # Highlight current word
                current_word_idx = min(i // frames_per_word, total_words - 1)
                x_offset = 100
                y_offset = height // 2

                for idx, word in enumerate(words):
                    color = highlight_color if idx == current_word_idx else text_color
                    rendered_text = font.render(word + " ", True, color)
                    text_rect = rendered_text.get_rect(topleft=(x_offset, y_offset))
                    screen.blit(rendered_text, text_rect)
                    x_offset += text_rect.width

                    # Wrap if text exceeds width
                    if x_offset > width - 200:
                        x_offset = 100
                        y_offset += text_rect.height + 20

                # Add blinking "Tap Here!" button (every 2s)
                if (i // fps) % 2 == 0:
                    button_font = pygame.font.SysFont("arial", 50, bold=True)
                    pygame.draw.rect(screen, (100, 100, 255), (width - 320, height - 150, 250, 80), 3)
                    button_text = button_font.render("Tap Here!", True, (100, 100, 255))
                    screen.blit(button_text, (width - 300, height - 135))

                # Save frame
                pygame.image.save(screen, f"{self.frames_dir}/frame_{i:04d}.png")

            # Combine frames + audio using ffmpeg
            os.system(
                f'ffmpeg -y -framerate {fps} -i {self.frames_dir}/frame_%04d.png '
                f'-i "{audio_path}" -c:v libx264 -pix_fmt yuv420p '
                f'-c:a aac -shortest "{output_path}"'
            )

            # Cleanup frames
            if os.path.exists(self.frames_dir):
                shutil.rmtree(self.frames_dir)

            print(f"✅ Video generated with subtitles: {output_path}")
            return output_path

        except Exception as e:
            print(f"❌ Error in VideoAgent: {e}")
            return None


# Run test
if __name__ == "__main__":
    agent = VideoAgent()
    agent.generate_video(
        "assets/narration.mp3",
        "Hey guys, today I want to talk about dogs and why they are amazing companions."
    )
