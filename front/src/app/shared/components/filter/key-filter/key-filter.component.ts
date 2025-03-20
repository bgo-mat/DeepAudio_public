import { Component, Input } from '@angular/core';
import {NgForOf} from "@angular/common";

@Component({
  selector: 'app-key-filter',
  standalone: true,
  templateUrl: './key-filter.component.html',
  styleUrls: ['./key-filter.component.scss'],
  imports: [
    NgForOf
  ]
})
export class KeyFilterComponent {
  @Input() keys: string[] = [];
  selectedKey: string | null = null;
  selectedScale: 'Major' | 'Minor' | null = null;

  selectKey(key: string) {
    this.selectedKey = key;
  }

  selectScale(scale: 'Major' | 'Minor') {
    this.selectedScale = scale;
  }
}
