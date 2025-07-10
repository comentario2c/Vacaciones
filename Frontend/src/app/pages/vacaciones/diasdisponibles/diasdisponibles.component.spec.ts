import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DiasdisponiblesComponent } from './diasdisponibles.component';

describe('DiasdisponiblesComponent', () => {
  let component: DiasdisponiblesComponent;
  let fixture: ComponentFixture<DiasdisponiblesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DiasdisponiblesComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(DiasdisponiblesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
