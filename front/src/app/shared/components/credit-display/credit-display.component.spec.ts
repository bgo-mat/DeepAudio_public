import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreditDisplayComponent } from './credit-display.component';

describe('CreditDisplayComponent', () => {
  let component: CreditDisplayComponent;
  let fixture: ComponentFixture<CreditDisplayComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreditDisplayComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CreditDisplayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
