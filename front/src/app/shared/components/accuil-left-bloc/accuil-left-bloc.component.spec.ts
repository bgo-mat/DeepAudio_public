import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AccuilLeftBlocComponent } from './accuil-left-bloc.component';

describe('AccuilLeftBlocComponent', () => {
  let component: AccuilLeftBlocComponent;
  let fixture: ComponentFixture<AccuilLeftBlocComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AccuilLeftBlocComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AccuilLeftBlocComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
