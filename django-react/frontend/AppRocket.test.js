import { render, screen } from '@testing-library/react';
import AppRocket from './AppRocket';

test('renders learn react link', () => {
  render(<AppRocket />);
  const linkElement = screen.getByText(/learn react/i);
  expect(linkElement).toBeInTheDocument();
});
