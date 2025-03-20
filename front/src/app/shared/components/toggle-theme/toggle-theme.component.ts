import {Component, OnInit, Renderer2} from '@angular/core';
import {MatSlideToggle} from "@angular/material/slide-toggle";
import {NgIf} from "@angular/common";

@Component({
  selector: 'app-theme-toggle',
  templateUrl: './toggle-theme.component.html',
  styleUrls: ['./toggle-theme.component.scss'],
  imports: [
    MatSlideToggle,
    NgIf
  ],
  standalone: true
})
export class ToggleThemeComponent implements OnInit {
  isDarkMode = false;

  constructor(private renderer: Renderer2) {}

  ngOnInit(): void {
    const storedTheme = localStorage.getItem('theme');

    if (storedTheme) {
      this.isDarkMode = storedTheme === 'dark';
    } else {
      // Détecte la préférence système
      this.isDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
    }

    this.applyTheme();
  }

  toggleTheme(): void {
    this.isDarkMode = !this.isDarkMode;
    this.applyTheme();
    localStorage.setItem('theme', this.isDarkMode ? 'dark' : 'light');
  }

  applyTheme(): void {
    if (this.isDarkMode) {
      this.renderer.addClass(document.documentElement, 'dark');
    } else {
      this.renderer.removeClass(document.documentElement, 'dark');
    }
  }
}
