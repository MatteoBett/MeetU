{
  description = "R development environment";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        
        rPackages = with pkgs.rPackages; [
          fmcsR
          igraph
          furrr
          purrr
          ChemmineR
        ];
      in {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            curl
            R
          ]++rPackages;
        };
      }
    );
}
