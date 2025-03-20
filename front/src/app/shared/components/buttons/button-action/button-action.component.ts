import {Component, Input} from '@angular/core';

@Component({
  selector: 'app-button-action',
  standalone: true,
  imports: [],
  templateUrl: './button-action.component.html',
  styleUrl: './button-action.component.scss'
})
export class ButtonActionComponent {
  @Input() name: string = 'Continue';
}
