import {Component, ElementRef, HostListener} from '@angular/core';
import {NgForOf, NgIf} from "@angular/common";
import {KeyFilterComponent} from "../key-filter/key-filter.component";
import {BpmFilterComponent} from "../bpm-filter/bpm-filter.component";
import {PackInfoComponent} from "../../detail-pack/pack-info/pack-info.component";

@Component({
  selector: 'app-filter-sounds',
  standalone: true,
  templateUrl: './filter-sounds.component.html',
  styleUrls: ['./filter-sounds.component.scss'],
  imports: [
    NgIf,
    NgForOf,
    KeyFilterComponent,
    BpmFilterComponent,
    PackInfoComponent
  ]
})
export class FilterSoundsComponent {
  isDropdownOpen: Record<string, boolean> = {
    instruments: false,
    genres: false,
    key: false,
    bpm: false,
  };


  instruments = [
    { name: 'Drums', count: 191908 },
    { name: 'Synth', count: 79579 },
    { name: 'Percussion', count: 44941 },
    { name: 'Vocals', count: 28222 },
  ];

  genres = ['Hip Hop', 'House', 'Trap', 'Rock', 'Jazz'];
  keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
  bpms = ['60-80', '80-100', '100-120', '120-140', '140-160'];

  constructor(private elementRef: ElementRef) {}

  toggleDropdown(filter: string) {
    this.isDropdownOpen[filter] = !this.isDropdownOpen[filter];

    // Close other dropdowns
    for (const key in this.isDropdownOpen) {
      if (key !== filter) {
        this.isDropdownOpen[key] = false;
      }
    }
  }

  closeAllDropdowns() {
    this.isDropdownOpen = {
      instruments: false,
      genres: false,
      key: false,
      bpm: false,
    };
  }

  @HostListener('document:click', ['$event'])
  handleClickOutside(event: Event) {
    const clickedInside = this.elementRef.nativeElement.contains(event.target);
    if (!clickedInside) {
      this.closeAllDropdowns();
    }
  }
}
