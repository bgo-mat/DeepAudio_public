import { Component } from '@angular/core';
import {NgIf} from "@angular/common";

@Component({
  selector: 'app-bpm-filter',
  standalone: true,
  templateUrl: './bpm-filter.component.html',
  styleUrls: ['./bpm-filter.component.scss'],
  imports: [
    NgIf
  ]
})
export class BpmFilterComponent {
  mode: 'Exact' | 'Range' = 'Exact';
  exactBpm: number | null = null;
  bpmRange: [number, number] = [50, 200];

  selectMode(mode: 'Exact' | 'Range') {
    this.mode = mode;
  }

  onExactBpmChange(event: Event) {
    const input = event.target as HTMLInputElement;
    this.exactBpm = input.value ? parseInt(input.value, 10) : null;
  }

  onRangeChange(event: Event, type: 'min' | 'max') {
    const input = event.target as HTMLInputElement;
    const value = input.valueAsNumber;

    if (type === 'min') {
      this.bpmRange[0] = value;
    } else if (type === 'max') {
      this.bpmRange[1] = value;
    }
  }

  clear() {
    // Réinitialiser le BPM exact et la plage de BPM
    this.exactBpm = null;
    this.bpmRange = [50, 200];
    this.mode = 'Exact';
  }
}
