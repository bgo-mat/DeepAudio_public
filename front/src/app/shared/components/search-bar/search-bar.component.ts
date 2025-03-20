import {AfterViewInit, Component, ElementRef, HostListener, ViewChild} from '@angular/core';
import {NgForOf, NgIf} from "@angular/common";
import {FormsModule} from "@angular/forms";

@Component({
  selector: 'app-search-bar',
  standalone: true,
  imports: [
    NgForOf,
    FormsModule,
    NgIf
  ],
  templateUrl: './search-bar.component.html',
  styleUrl: './search-bar.component.scss'
})
export class SearchBarComponent implements AfterViewInit {

  suggestions: string[] = ['New Arrivals', 'Ladies', 'Mens', 'Accessories', 'Sale'];
  selectedKeywords: string[] = [];
  @ViewChild('scrollContainer') private scrollContainer!: ElementRef;
  inputValue = '';
  showLeftShadow = false;
  showRightShadow = false;

  ngAfterViewInit() {
    this.checkForOverflow();
    this.onScroll(); // Initial check based on initial scroll position
  }

  @HostListener('window:resize')
  onResize() {
    this.checkForOverflow();
    this.onScroll();
  }

  checkForOverflow() {
    const container = this.scrollContainer.nativeElement;
    this.showLeftShadow = false;
    this.showRightShadow = false;

    if (container.scrollWidth > container.clientWidth) {
      this.showRightShadow = true;
    }
  }

  onScroll() {
    const container = this.scrollContainer.nativeElement;
    const scrollLeft = container.scrollLeft;
    const maxScrollLeft = container.scrollWidth - container.clientWidth;

    // Afficher l'ombre gauche si on n'est pas au début
    this.showLeftShadow = scrollLeft > 0;

    // Afficher l'ombre droite si on n'est pas à la fin
    this.showRightShadow = scrollLeft < maxScrollLeft;
  }

  addKeyword(keyword: string) {
    if (!this.selectedKeywords.includes(keyword)) {
      this.selectedKeywords.push(keyword);
      setTimeout(() => this.scrollToEnd(), 100);
    }
  }

  removeKeyword(keyword: string) {
    this.selectedKeywords = this.selectedKeywords.filter(k => k !== keyword);
  }

  onInputKeyDown(event: KeyboardEvent) {
    if (event.key === 'Enter' && this.inputValue.trim() !== '') {
      this.addKeyword(this.inputValue.trim());
      this.inputValue = '';
      event.preventDefault();
    }
  }

  onSubmit() {
    console.log('Mots-clés recherchés :', this.selectedKeywords);
  }

  private scrollToEnd(): void {
    try {
      const container = this.scrollContainer.nativeElement;
      container.scrollLeft = container.scrollWidth;
    } catch (err) {
      console.error('Erreur lors du défilement :', err);
    }
  }
}
